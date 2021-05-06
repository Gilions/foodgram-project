from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, HiddenField

from apps.recipes.models import Cart, Composition, Favorite, Follow


class ComponentsSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='name')
    dimension = serializers.ReadOnlyField(source='unit')

    class Meta:
        model = Composition
        fields = ['title', 'dimension']


class FollowSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('user', 'author',)

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            user = data['user']
            author = data['author']
            if Follow.objects.filter(user=user, author=author).exists():
                raise serializers.ValidationError('Вы уже подписаны на автора')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('user', 'recipe', )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            user = data['user']
            recipe = data['recipe']
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                raise serializers.ValidationError(
                    'Вы уже добавли рецепт в избранные')
        return data


class PurchasesSerializer(serializers.ModelSerializer):
    customer = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ('customer', 'item', )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            customer = data['customer']
            item = data['item']
            if Cart.objects.filter(customer=customer, item=item).exists():
                raise serializers.ValidationError(
                    'Вы уже добавли рецепт в корзину')
        return data
