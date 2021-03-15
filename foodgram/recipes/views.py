from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *


def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        "paginator": paginator
    }
    return render(request, 'index.html', context)