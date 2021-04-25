from django.urls import path

from apps.api.views import ComponentsViewSet, subscription, favorite, purchases

urlpatterns = [
    path('ingredients/', ComponentsViewSet.as_view()),

    path('subscriptions/', subscription, name='subscribe'),
    path('subscriptions/<int:author_id>', subscription, name='unsubscribe'),

    path('favorites/', favorite, name='favorite'),
    path('favorites/<int:recipe_id>', favorite, name='favorite'),

    path('purchases/', purchases, name='add_purchases'),
    path('purchases/<int:recipe_id>', purchases, name='remove_purchases'),
]
