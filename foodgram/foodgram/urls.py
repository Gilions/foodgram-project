"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

from foodgram import settings


handler404 = "apps.about.views.page_not_found" # noqa
handler500 = "apps.about.views.server_error" # noqa


urlpatterns = [
    # Регистрация/авторизация
    path("auth/", include("apps.users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    # Админка
    path('admin/', admin.site.urls),
    path('about/', include("apps.about.urls")),

    path('api/', include("apps.api.urls")),

    # Остальные урлы
    path('', include('apps.recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
