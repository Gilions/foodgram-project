from decimal import Decimal

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.utils import json

from .models import *
from .forms import RecipeForm
from .serializers import ComponentsSerializer


TAGS = ['breakfast', 'lunch', 'dinner']


def index(request):
    tags = Tag.objects.all()
    tags_list = request.GET.getlist('tag', TAGS)
    recipe_list = Recipe.objects.filter(
        tag__name__in=tags_list
    ).prefetch_related(
        'tag'
    ).select_related('author').distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': tags,
        'page': page,
        "paginator": paginator
    }
    return render(request, 'index.html', context)


class ComponentsViewSet(generics.ListAPIView):
    # Поиск данных по таблице Components
    serializer_class = ComponentsSerializer
    def get_queryset(self):
        data = self.request.GET['query']
        if data is not None:
            queruset = Components.objects.filter(name__istartswith=data)
            return queruset
        return Components.objects.none()


def create(request):
    # Создаем новый рецепт
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        # Проверяем наличие ингредиентов
        if 'nameIngredient_1' not in request.POST:
            form.add_error(None, 'Необходимо указать ингредиенты!')
        else:
            # Создаем рецепт
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                # Подвязываем Теги
                for tag in form.cleaned_data['tag']:
                    instance.tag.add(tag.id)
                # Получаем ингредиенты
                ingredients = []
                for key, value in form.data.items():
                    if 'nameIngredient' in key:
                        name = value
                    if 'valueIngredient' in key:
                        amount = Decimal(value.replace(',', '.'))
                        ingredient = get_object_or_404(
                            Components, name=name)
                        ingredients.append(
                            Amount(ingredient=ingredient, recipe=instance, amount=amount)
                        )
            # Записываем данные в таблицу
            Amount.objects.bulk_create(ingredients)
            return redirect('index')

    form = RecipeForm()
    context = {
        'form': form,
    }
    return render(request, 'form_recipe.html', context)


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    context = {
        'recipe': recipe,
    }
    return render(request, 'recipe_page.html', context)


def author_view(request, username):
    # Рецепты автора
    author = get_object_or_404(User, username=username)
    recipe_list = Recipe.objects.filter(author=author)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        "paginator": paginator
    }
    return render(request, 'author_recipe.html', context)


def follow(request):
    # Подписка на автора
    if request.method == 'POST':
        id = json.loads(request.body.decode())['id']
        author = get_object_or_404(User, id=id)

        # Отсеиваем возможность подписаться на самого себя, либо прозвести дубль
        sub = Follow.objects.filter(user=request.user, author=author).exists()
        if request.user == author or sub:
            return redirect('author_recipe', author.username)

        Follow.objects.create(user=request.user, author=author)
        return JsonResponse({'success': True})


def unfollow(request, id):
    # Отписываемся
    author = get_object_or_404(User, id=id)
    Follow.objects.filter(user=request.user, author=author).delete()
    return JsonResponse({'success': True})


def follow_index(request):
    author_list = request.user.follower.all()

    paginator = Paginator(author_list , 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        "paginator": paginator
    }
    return render(request, 'my_follow.html', context)


def add_favorite(request):
    if request.method == 'POST':
        id = json.loads(request.body.decode())['id']
        recipe = get_object_or_404(Recipe, id=id)
        actual_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
        if actual_favorite is False:
            Favorite.objects.create(user=request.user, recipe=recipe)
            recipe.fav_counter += 1
            recipe.save()
            return JsonResponse({'success': True})


def remove_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    recipe.fav_counter -= 1
    recipe.save()
    return JsonResponse({'success': True})



def favorite_index(request):

    recipe_list = Recipe.objects.filter(related_recipes__user=request.user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        "paginator": paginator
    }
    return render(request, 'favorite.html', context)
