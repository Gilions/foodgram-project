from django.contrib import admin

from .models import Amount, Cart, Composition, Favorite, Follow, Recipe, Tag

admin.site.register(Amount)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(Cart)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'time_cooking', 'description',
        'pub_date', 'fav_counter'
    )

    list_filter = ("name",)


@admin.register(Composition)
class ComponentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit',)
    list_filter = ('name',)
