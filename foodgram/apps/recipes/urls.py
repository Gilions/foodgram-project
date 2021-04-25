from django.urls import path

from .views import create, recipe_edit, recipe_delete,\
    follow_index, cart,\
    favorite_index, remove_recipe_from_cart,\
    download, recipe_view, author_view, index


urlpatterns = [
    path('create/', create, name='create'),
    path('recipe/<slug:slug>/edit/', recipe_edit, name='recipe_edit'),
    path('recipe/<slug:slug>/delete/', recipe_delete, name='recipe_delete'),

    path('following/', follow_index, name='follow'),

    path('my_favorite', favorite_index, name='my_favorite'),

    path('cart/', cart, name='cart'),
    path('cart/<int:recipe_id>', remove_recipe_from_cart,
         name='remove_recipe_from_cart'),

    path('download/', download, name='download'),

    path('recipe/<slug:slug>/', recipe_view, name='recipe'),
    path('recipe/author/<str:username>/', author_view, name='author_recipe'),
    path('', index, name='index'),
]
