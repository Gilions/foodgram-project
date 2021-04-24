from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.utils import json
import datetime as dt

from .models import Tag, Recipe, Cart, \
    User, Favorite, Follow, Components, Amount
from .forms import RecipeForm
from .serializers import ComponentsSerializer
from .utility import download_pdf, check, get_tags

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


@login_required
def follow_index(request):
    author_list = request.user.follower.all()

    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        "paginator": paginator
    }
    return render(request, 'my_follow.html', context)


@login_required
def favorite_index(request):
    tags = Tag.objects.all()
    tags_list = request.GET.getlist('tag', TAGS)
    recipe_list = Recipe.objects.filter(
        related_recipes__user=request.user,
        tag__name__in=tags_list
    ).prefetch_related('tag').select_related('author').distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': tags,
        'page': page,
        "paginator": paginator
    }
    return render(request, 'favorite.html', context)


@login_required
def cart(request):
    context = {
        'recipes': request.user.purchases.all(),
    }
    return render(request, 'cart.html', context)


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
    return render(request, 'author_recipes.html', context)


@login_required
def create(request):
    form = RecipeForm()

    # Создаем новый рецепт
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if not get_tags(request):
            form.add_error(None, "Необходимо выбрать тип блюда!")
        if check(request):
            form.add_error(None, "Необходимо добавить ингредиенты!")

        # Создаем рецепт
        if form.is_valid():
            with transaction.atomic():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()

                tags = get_tags(request)
                for i in tags:
                    tag = Tag.objects.get(name=i)
                    instance.tag.add(tag.id)

                add_m2m(request, form, instance)
                return redirect('recipe',  instance.slug)
    context = {
        'form': form,
    }
    return render(request, 'form_recipe.html', context)


@login_required
def recipe_edit(request, slug):
    edit = True
    recipe = get_object_or_404(Recipe, slug=slug)

    if not request.user.is_superuser:
        if recipe.author != request.user:
            return redirect('recipe', recipe.slug)

    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)

    if request.method == 'POST':

        if not get_tags(request):
            form.add_error(None, "Необходимо выбрать тип блюда!")
        if check(request):
            form.add_error(None, "Необходимо добавить ингредиенты!")

        if form.is_valid():
            with transaction.atomic():
                instance = form.save(commit=False)
                instance.pub_date = dt.datetime.now()
                instance.tag.clear()
                instance.save()
                # Чистим не нужные ингредиенты
                Amount.objects.filter(recipe=instance).delete()
                # Добавляем Теги/Ингредиенты
                add_m2m(request, form, instance)
                return redirect('recipe', recipe.slug)
    context = {
        'edit': edit,
        'recipe': recipe,
        'form': form,
        'tags': recipe.tag.all()
    }
    return render(request, 'form_recipe.html', context)


def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if not request.user.is_superuser:
        if request.user != recipe.author:
            return redirect('recipe', recipe.slug)

    recipe.delete()
    return redirect('author_recipe', request.user.username)


@login_required
def subscription(request, author_id=None):
    # Subscribe to author
    if request.method == 'POST':
        get_id = json.loads(request.body.decode())['id']
        author = get_object_or_404(User, id=get_id)
        # Check permission
        sub = Follow.objects.filter(user=request.user, author=author).exists()
        if request.user == author or sub:
            return redirect('author_recipe', author.username)

        Follow.objects.create(user=request.user, author=author)
        return JsonResponse({'success': True})

    if request.method == 'DELETE':
        author = get_object_or_404(User, id=author_id)
        Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({'success': True})


@login_required
def favorite(request, recipe_id=None):
    if request.method == 'POST':
        get_id = json.loads(request.body.decode())['id']
        recipe = get_object_or_404(Recipe, id=get_id)
        check = Favorite.objects.filter(
            user=request.user, recipe=recipe).exists()
        if check is False:
            Favorite.objects.create(user=request.user, recipe=recipe)
            recipe.fav_counter += 1
            recipe.save()
            return JsonResponse({'success': True})

    if request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favorite.objects.filter(user=request.user, recipe=recipe).delete()
        recipe.fav_counter -= 1
        recipe.save()
        return JsonResponse({'success': True})


@login_required
def purchases(request, recipe_id=None):
    if request.method == 'POST':
        get_id = json.loads(request.body.decode())['id']
        recipe = get_object_or_404(Recipe, id=get_id)
        check = Cart.objects.filter(
            item=recipe, customer=request.user).exists()
        if check is False:
            Cart.objects.create(item=recipe, customer=request.user)
            return JsonResponse({'success': True})

    if request.method == "DELETE":
        recipes = get_object_or_404(Recipe, id=recipe_id)
        Cart.objects.filter(item=recipes, customer=request.user).delete()
        return JsonResponse({'success': True})


def remove_recipe_from_cart(request, recipe_id):
    recipes = get_object_or_404(Recipe, id=recipe_id)
    Cart.objects.filter(item=recipes, customer=request.user).delete()
    return redirect('cart')


def download(request):
    data = request.user.purchases.select_related(
                'item'
            ).order_by(
                'item__ingredients__name'
            ).values(
                'item__ingredients__name', 'item__ingredients__unit'
            ).annotate(amount=Sum('item__recipe_ingredients__amount')).all()

    return download_pdf(data)


class ComponentsViewSet(generics.ListAPIView):
    # Search ingredients
    serializer_class = ComponentsSerializer

    def get_queryset(self):
        data = self.request.GET['query']
        if data is not None:
            queryset = Components.objects.filter(name__istartswith=data)
            return queryset


def add_m2m(request, form, recipe):
    # Add ingredients
    ingredients = []
    name = None
    for key, value in form.data.items():
        if 'nameIngredient' in key:
            name = value
        if 'valueIngredient' in key:
            amount = Decimal(value.replace(',', '.'))
            ingredient = get_object_or_404(
                Components, name=name)
            ingredients.append(
                Amount(
                    ingredient=ingredient,
                    recipe=recipe,
                    amount=amount
                )
            )
    Amount.objects.bulk_create(ingredients)
