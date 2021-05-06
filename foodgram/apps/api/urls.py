from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ComponentsViewSet, FavoriteViewSet, FollowViewSet,
                    PurchasesViewSet)

router_v1 = DefaultRouter()

router_v1.register('subscriptions', FollowViewSet, basename='subscriptions')
router_v1.register('favorites', FavoriteViewSet, basename='favorites')
router_v1.register('purchases', PurchasesViewSet, basename='purchases')
router_v1.register('ingredients', ComponentsViewSet, basename='ingredients')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
