from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


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
    '!': '',
}


def translate_rus_eng(text):
    # Заменяем русские буквы английскими
    symbols = ['+', '-', ';', '.', ',', '(', ')', '*', '=', '/', '"', "'", ':']
    for index in symbols:
        text = text.replace(index, '')
    format_text = '{}'.format(text).lower()
    return ''.join(letters.get(x, x) for x in format_text)


def download_pdf(data):
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
