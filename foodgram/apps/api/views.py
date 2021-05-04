from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.utils import json

from apps.recipes.models import (Cart, Composition, Favorite, Follow, Recipe,
                                 User)
from apps.api.serializers import ComponentsSerializer


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
    # Remove from subscriptions
    if request.method == 'DELETE':
        author = get_object_or_404(User, id=author_id)
        Follow.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({'success': True})


@login_required
def favorite(request, recipe_id=None):
    # Adds to favorite
    if request.method == 'POST':
        get_id = json.loads(request.body.decode())['id']
        recipe = get_object_or_404(Recipe, id=get_id)
        # Check permission
        check = Favorite.objects.filter(
            user=request.user, recipe=recipe).exists()
        if check is False:
            Favorite.objects.create(user=request.user, recipe=recipe)
            recipe.fav_counter += 1
            recipe.save()
            return JsonResponse({'success': True})
    # Remove from purchases
    if request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Favorite.objects.filter(user=request.user, recipe=recipe).delete()
        recipe.fav_counter -= 1
        recipe.save()
        return JsonResponse({'success': True})


@login_required
def purchases(request, recipe_id=None):
    # Adds to purchases
    if request.method == 'POST':
        get_id = json.loads(request.body.decode())['id']
        recipe = get_object_or_404(Recipe, id=get_id)
        check = Cart.objects.filter(
            item=recipe, customer=request.user).exists()
        if check is False:
            Cart.objects.create(item=recipe, customer=request.user)
            return JsonResponse({'success': True})
    # Remove from purchases
    if request.method == "DELETE":
        recipes = get_object_or_404(Recipe, id=recipe_id)
        Cart.objects.filter(item=recipes, customer=request.user).delete()
        return JsonResponse({'success': True})


class ComponentsViewSet(generics.ListAPIView):
    # Search ingredients
    serializer_class = ComponentsSerializer

    def get_queryset(self):
        data = self.request.GET['query']
        if data is not None:
            queryset = Composition.objects.filter(name__istartswith=data)
            return queryset
