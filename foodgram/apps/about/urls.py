from django.urls import path

from apps.about.views import About, About_assistant, About_tech

urlpatterns = [
    path('', About.as_view(), name='about'),
    path('tach/', About_tech.as_view(), name='tech'),
    path('assistant/', About_assistant.as_view(), name='assistant'),
]
