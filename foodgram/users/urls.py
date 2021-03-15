from django.urls import path
from . import views

urlpatterns = [
    # Регистрация
    path("signup/", views.SignUp.as_view(), name="signup")
]