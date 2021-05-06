from django.urls import path

from apps.about.views import About, AboutAssistant, AboutTech

urlpatterns = [
    path('', About.as_view(), name='about'),
    path('tech/', AboutTech.as_view(), name='tech'),
    path('assistant/', AboutAssistant.as_view(), name='assistant'),
]
