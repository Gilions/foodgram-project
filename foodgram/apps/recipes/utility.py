from django.db import transaction
from django.http import HttpResponse


from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime as dt


letters = {
    'ь': '',
    'ъ': '',
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ы': 'yi',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    ' ': '_',
    '-': '_',
}


def translate_rus_eng(text):
    # Replacing Russian letters, english
    symbols = [
        '+', '-', ';', '.', ',', '(', ')', '*',
        '=', '/', '"', "'", ':', '!', '?'
    ]
    for index in symbols:
        text = text.replace(index, '')
    format_text = '{}'.format(text).lower()
    return ''.join(letters.get(x, x) for x in format_text)


def download_pdf(data):
    # Download shopping list in pdf format
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="List product.pdf"'

    p = canvas.Canvas(response)
    p.setFont('DejaVuSans', 15)
    p.drawString(100, 800, "Список продуктов:")
    p.setFont('DejaVuSans', 10)
    x, y = 10, 780
    for item in data:
        p.drawString(x, y, item.get('item__ingredients__name')
                     + ' ' + '(' + item.get('item__ingredients__unit') + ')'
                     + ' - ' + str(item.get('amount')))
        y -= 15

    p.showPage()
    p.save()
    return response


def check(request, form):
    # Check validations fields
    ingredient = False
    tags = False
    for key in request.POST.keys():
        if 'nameIngredient' in key:
            ingredient = True
        if key in ['breakfast', 'lunch', 'dinner']:
            tags = True
    if not ingredient:
        form.add_error(None, "Необходимо добавить ингредиенты!")
    if not tags:
        form.add_error(None, "Необходимо выбрать тип блюда!")


def get_tags(request):
    # Get tags field
    tags_list = []
    for key in request.POST.keys():
        if key in ['breakfast', 'lunch', 'dinner']:
            tags_list.append(key)
    return tags_list


def new_recipe(request, form):
    # Create a new recipe
    check(request, form)
    if form.is_valid():
        with transaction.atomic():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return instance


def edit_recipe(request, form):
    # Edit recipe
    check(request, form)
    if form.is_valid():
        with transaction.atomic():
            instance = form.save(commit=False)
            instance.pub_date = dt.datetime.now()
            instance.tag.clear()
            instance.save()
            return instance
