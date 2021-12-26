from django.urls import path
from . import views

app_name = "registration"

urlpatterns = [
    path("", views.index, name="index"),
    path("program_reg", views.program_reg, name="program_reg"),
    path("user_reg", views.user_reg, name="user_reg"),
    path("user_logout", views.user_logout, name="user_logout")
]