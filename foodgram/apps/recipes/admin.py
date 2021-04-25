from django.contrib import admin
from .models import Recipe, Components, Amount, Tag, Follow, Favorite, Cart
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


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


@admin.register(Components)
class ComponentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit',)
    list_filter = ('name',)


class MyUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('groups__name', 'email', 'is_active',)


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
