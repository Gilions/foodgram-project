from django import template

from recipes.models import Follow, Favorite

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def sub_to(user, author):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def fav_to(user, recipe):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()
