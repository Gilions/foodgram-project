from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class MyUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + (
        'groups__name', 'email', 'is_active',
    )


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
