from django.forms import ModelForm, TextInput, Textarea
from django import forms

from .models import Recipe, Components


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'image', 'time_cooking', 'description', 'tag']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form__input'
            }),
            'tag': forms.CheckboxSelectMultiple(attrs={
                'class': 'tags__checkbox tags__checkbox_active '}),
            'time_cooking': TextInput(attrs={
                'class': 'form__input'
            }),
            'description': Textarea(attrs={
                'rows': 8,
                'class': 'form__textarea'
            }),
        }
