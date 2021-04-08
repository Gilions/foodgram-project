from rest_framework import serializers

from .models import Components, Follow


class ComponentsSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='name')
    dimension = serializers.ReadOnlyField(source='unit')
    class Meta:
        model = Components
        fields = ['title', 'dimension']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['user', 'author']