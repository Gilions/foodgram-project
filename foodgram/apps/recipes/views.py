from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import PAGINATION_PAGE_SIZE, TAGS
from .forms import RecipeForm
from .models import Amount, Cart, Composition, Recipe, Tag, User
from .utility import download_pdf, edit_recipe, get_tags, new_recipe, tags_filter


def index(request):
    # The main page of the site.
    recipe_list = Recipe.objects.filter(
        tags__name__in=tags_filter(request)
    ).prefetch_related(
        'tags'
    ).select_related('author').distinct()
    paginator = Paginator(recipe_list, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': Tag.objects.all(),
        'page': page,
        "paginator": paginator
    }
    return render(request, 'index.html', context)


@login_required
def follow_index(request):
    # The subscriber page is displayed.
    author_list = request.user.follower.all()

    paginator = Paginator(author_list, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        "paginator": paginator
    }
    return render(request, 'my_follow.html', context)


@login_required
def favorite_index(request):
    # The favorite recipe page is displayed.
    recipe_list = Recipe.objects.filter(
        favorite__user=request.user,
        tags__name__in=tags_filter(request)
    ).prefetch_related('tags').select_related('author').distinct()

    paginator = Paginator(recipe_list, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': Tag.objects.all(),
        'page': page,
        "paginator": paginator
    }
    return render(request, 'favorite.html', context)


def author_view(request, username):
    # Authors recipes.
    tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    recipe_list = Recipe.objects.filter(
        author=author,
        tags__name__in=tags_filter(request)
    ).prefetch_related('tags').select_related('author').distinct()
    paginator = Paginator(recipe_list, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': tags,
        'author': author,
        'page': page,
        "paginator": paginator
    }
    return render(request, 'author_recipes.html', context)


@login_required
def cart(request):
    # Site cart.
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


@login_required
def create(request):
    # Create new recipe
    form = RecipeForm(request.POST or None, request.FILES)
    recipe = new_recipe(request, form)
    # Adds tags
    if recipe:
        tags = get_tags(request)
        for i in tags:
            tag = Tag.objects.get(name=i)
            recipe.tags.add(tag.id)
        # Adds ingredients
        get_ingredients(request, form, recipe)
        return redirect('recipe',  recipe.slug)
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
        instance = edit_recipe(request, form)
        if instance:
            # Remove unnecessary ingredients
            Amount.objects.filter(recipe=instance).delete()
            # Adds tags
            tags = get_tags(request)
            for i in tags:
                tag = Tag.objects.get(name=i)
                instance.tags.add(tag.id)
            # Adds ingredients
            get_ingredients(request, form, instance)

            return redirect('recipe', recipe.slug)
    context = {
        'edit': edit,
        'recipe': recipe,
        'form': form,
        'tags': recipe.tags.all()
    }
    return render(request, 'form_recipe.html', context)


def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if not request.user.is_superuser:
        if request.user != recipe.author:
            return redirect('recipe', recipe.slug)

    recipe.delete()
    return redirect('author_recipe', request.user.username)


def remove_recipe_from_cart(request, recipe_id):
    # Removes selected recipes from the cart.
    recipes = get_object_or_404(Recipe, id=recipe_id)
    Cart.objects.filter(item=recipes, customer=request.user).delete()
    return redirect('cart')


def download(request):
    # The request loads the ingredients of the selected recipes.
    # And their amount.
    data = request.user.purchases.select_related(
                'item'
            ).order_by(
                'item__ingredients__name'
            ).values(
                'item__ingredients__name', 'item__ingredients__unit'
            ).annotate(amount=Sum('item__recipe_ingredients__amount')).all()

    return download_pdf(data)


def get_ingredients(request, form, recipe):
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
