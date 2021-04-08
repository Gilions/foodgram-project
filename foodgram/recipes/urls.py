from django.urls import path

from .views import *


urlpatterns = [

    path('ingredients/', ComponentsViewSet.as_view()),

    path('create/', create, name='create'),

    path('subscriptions/', follow, name='subscribe'),
    path('subscriptions/<int:id>', unfollow, name='unsubscribe'),
    path('following/', follow_index, name='follow'),

    path('favorites/', add_favorite, name='add_fav'),
    path('favorites/<int:id>', remove_favorite, name='rem_fav'),
    path('my_favorite', favorite_index, name='my_favorite'),

    path('recipe/<slug:slug>/', recipe_view, name='recipe'),
    path('recipe/author/<str:username>/', author_view, name='author_recipe'),
    path('', index, name='index'),
]