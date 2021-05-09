from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers import (ComponentsSerializer, FavoriteSerializer,
                                  FollowSerializer, PurchasesSerializer)
from apps.recipes.models import Cart, Composition, Favorite, Follow, Recipe


class CreateDestroyMethod(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class FollowViewSet(CreateDestroyMethod):
    """
    Save or delete subscribes

    Table:
        Follow
    Available methods:
        POST, DELETE
    Args:
        author: id
    """
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    lookup_field = 'author'

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Follow,
                                     user=request.user,
                                     author=kwargs.get('author')
                                     )
        self.perform_destroy(instance)
        content = {'success': True}
        return Response(content, status=status.HTTP_200_OK)


class FavoriteViewSet(CreateDestroyMethod):
    """
    Save or delete favorites recipe

    Table:
        Favorite
    Available methods:
        POST, DELETE
    Args:
        recipe: id
    """
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        id = serializer.data['recipe']
        recipe = get_object_or_404(Recipe, id=id)
        recipe.fav_counter += 1
        recipe.save()

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Favorite,
                                     user=request.user,
                                     recipe=kwargs.get('recipe')
                                     )
        id = self.kwargs['recipe']
        recipe = get_object_or_404(Recipe, id=id)
        recipe.fav_counter -= 1
        recipe.save()
        self.perform_destroy(instance)
        content = {'success': True}
        return Response(content, status=status.HTTP_200_OK)


class PurchasesViewSet(CreateDestroyMethod):
    """
    Add or remove recipes from cart

    Table:
        Cart
    Available methods:
        POST, DELETE
    Args:
        item: id
    """
    queryset = Cart.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PurchasesSerializer
    lookup_field = 'item'

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Cart,
                                     customer=request.user,
                                     item=kwargs.get('item')
                                     )
        self.perform_destroy(instance)
        content = {'success': True}
        return Response(content, status=status.HTTP_200_OK)


class ComponentsViewSet(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Search ingredients
    Table:
        Composition
    Available methods:
        GET
    Args:
        query params
    """
    serializer_class = ComponentsSerializer

    def get_queryset(self):
        data = self.request.GET['query']
        if data is not None:
            queryset = Composition.objects.filter(name__istartswith=data)
            return queryset
        return Composition.objects.none()
