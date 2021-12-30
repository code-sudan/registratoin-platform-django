from django.urls import path
from . import views

app_name = "registration"

urlpatterns = [
    path("", views.index, name="index"),
    path("register_student/", views.register_student, name="register_student"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("student_details/", views.student_details, name="student_details"),
    path("program_registration/", views.program_registration, name='program_registration'),
]