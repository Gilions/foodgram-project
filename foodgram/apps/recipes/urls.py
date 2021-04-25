from django.urls import path

from .views import create, recipe_edit, recipe_delete,\
    follow_index, cart,\
    favorite_index, remove_recipe_from_cart,\
    download, recipe_view, author_view, index


urlpatterns = [
    # Create and edit recipes
    path('create/', create, name='create'),
    path('recipe/<slug:slug>/edit/', recipe_edit, name='recipe_edit'),
    path('recipe/<slug:slug>/delete/', recipe_delete, name='recipe_delete'),

    # Pages of the author and recipe
    path('recipe/<slug:slug>/', recipe_view, name='recipe'),
    path('recipe/author/<str:username>/', author_view, name='author_recipe'),

    # Follow and favorite index pages
    path('following/', follow_index, name='follow'),
    path('my_favorite', favorite_index, name='my_favorite'),

    # Works with a cart of the site
    path('cart/', cart, name='cart'),
    path('cart/<int:recipe_id>', remove_recipe_from_cart,
         name='remove_recipe_from_cart'),
    path('download/', download, name='download'),

    # Index page
    path('', index, name='index'),
]
