from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'image', 'time_cooking', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form__input'
            }),
            'time_cooking': forms.TextInput(attrs={
                'class': 'form__input'
            }),
            'description': forms.Textarea(attrs={
                'rows': 8,
                'class': 'form__textarea'
            }),
        }
