from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Components)
admin.site.register(Amount)
admin.site.register(Tag)

