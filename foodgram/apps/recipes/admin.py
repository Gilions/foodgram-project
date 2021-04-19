from django.contrib import admin
from .models import Recipe, Components, Amount, Tag, Follow, Favorite, Cart

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Components)
admin.site.register(Amount)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(Cart)
