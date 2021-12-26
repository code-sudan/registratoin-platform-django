from django.urls import path
from . import views

app_name = "registration"

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("signup", views.signup, name="signup"),
]