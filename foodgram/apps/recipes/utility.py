import datetime as dt
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import TAGS

from .models import Amount, Composition, Tag


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


def tags_filter(request):
    # Get actual tags
    tags_list = request.GET.getlist('tag', TAGS)
    return tags_list


def check(request, form):
    # Check validations fields
    ingredient = False
    tags = False
    for key, value in request.POST.items():
        if 'valueIngredient' in key and int(value) <= 0:
            form.add_error(None,
                           "Количество ингредиента должно быть больше 0.")
        if 'nameIngredient' in key:
            ingredient = True
        if key in TAGS:
            tags = True
    if not ingredient:
        form.add_error(None, "Необходимо добавить ингредиенты!")
    if not tags:
        form.add_error(None, "Необходимо выбрать тип блюда!")


def get_tags(request):
    # Get tags list
    tags_list = []
    for key in request.POST.keys():
        if key in TAGS:
            tags_list.append(key)
    return tags_list


def get_ingredients(form, recipe):
    # Add Ingredients to New Recipe.
    ingredients = []
    name = None
    for key, value in form.data.items():
        if 'nameIngredient' in key:
            name = value
        if 'valueIngredient' in key:
            amount = Decimal(value.replace(',', '.'))
            ingredient = get_object_or_404(
                Composition, name=name)
            ingredients.append(
                Amount(
                    ingredient=ingredient,
                    recipe=recipe,
                    amount=amount
                )
            )
    Amount.objects.bulk_create(ingredients)


def save_recipe(request, form, edit=None):
    # The function writes a recipe to the database or edits it.
    if request.POST:
        check(request, form)
    try:
        if form.is_valid():
            with transaction.atomic():
                recipe = form.save(commit=False)
                if edit:
                    recipe.pub_date = dt.datetime.now()
                    recipe.tags.clear()
                else:
                    recipe.author = request.user
                recipe.save()
            # Adds tags to the recipe
            for index in get_tags(request):
                tag = get_object_or_404(Tag, name=index)
                recipe.tags.add(tag.id)

            if edit:
                Amount.objects.filter(recipe=recipe).delete()
            # Adds ingredients to the recipe
            get_ingredients(form, recipe)
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest
