from django.urls import path

from apps.api.views import ComponentsViewSet, favorite, purchases, subscription

urlpatterns = [
    path('v1/ingredients/', ComponentsViewSet.as_view()),

    path('v1/subscriptions/', subscription, name='subscribe'),
    path('v1/subscriptions/<int:author_id>/', subscription, name='unsubscribe'),

    path('v1/favorites/', favorite, name='favorite'),
    path('v1/favorites/<int:recipe_id>/', favorite, name='favorite'),

    path('v1/purchases/', purchases, name='add_purchases'),
    path('v1/purchases/<int:recipe_id>/', purchases, name='remove_purchases'),
]
