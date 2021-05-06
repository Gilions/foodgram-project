from django.urls import path

from . import views

urlpatterns = [
    # Registrations.
    path("signup/", views.SignUp.as_view(), name="signup")
]
