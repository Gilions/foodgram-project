from django.urls import path

from .views import create, ComponentsViewSet, recipe_edit, recipe_delete,\
    follow_index, subscription, favorite, cart,\
    favorite_index, remove_recipe_from_cart, purchases,\
    download, recipe_view, author_view, index


urlpatterns = [

    path('ingredients/', ComponentsViewSet.as_view()),

    path('create/', create, name='create'),
    path('recipe/<slug:slug>/edit/', recipe_edit, name='recipe_edit'),
    path('recipe/<slug:slug>/delete/', recipe_delete, name='recipe_delete'),

    path('subscriptions/', subscription, name='subscribe'),
    path('subscriptions/<int:author_id>', subscription, name='unsubscribe'),
    path('following/', follow_index, name='follow'),

    path('favorites/', favorite, name='favorite'),
    path('favorites/<int:recipe_id>', favorite, name='favorite'),
    path('my_favorite', favorite_index, name='my_favorite'),

    path('cart/', cart, name='cart'),
    path('cart/<int:id>', remove_recipe_from_cart,
         name='remove_recipe_from_cart'),
    path('purchases/', purchases, name='add_purchases'),
    path('purchases/<int:recipe_id>', purchases, name='remove_purchases'),
    path('download/', download, name='download'),

    path('recipe/<slug:slug>/', recipe_view, name='recipe'),
    path('recipe/author/<str:username>/', author_view, name='author_recipe'),
    path('', index, name='index'),
]
