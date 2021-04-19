from django.forms import ModelForm, TextInput, Textarea

from .models import Recipe


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'image', 'time_cooking', 'description']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form__input'
            }),
            'time_cooking': TextInput(attrs={
                'class': 'form__input'
            }),
            'description': Textarea(attrs={
                'rows': 8,
                'class': 'form__textarea'
            }),
        }
