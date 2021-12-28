from django.forms.fields import CharField
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from secrets import randbelow
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student

# Create your views here.



USER_PASSWORD = "codesudan"

@login_required(login_url="login/")
def index(request):
    return HttpResponse("This is index, if you see this you're logged in")


# registration and login form form
class register_login_form(forms.Form):
    phone_number = CharField(max_length=12, label="الرجاء إدخال رقم تلفونك", required=True, initial="0912345678")

def login_view(request):
    if request.method == "GET":
        return render(request, "registration/login_student.html", {
            "form": register_login_form()
        })
    elif request.method == "POST":
        form = register_login_form(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            phone_number = f"249{phone_number[-9:]}"
            if len(phone_number) < 10:
                return render(request, "registration/login_student.html", {
                    "form": form,
                    "error_message": "الرجاء إدخال رقم التلفون بالهئة 0912345678"
                })
            else:
                student = authenticate(request, username=phone_number, password=USER_PASSWORD, is_complete=False)
                if student is not None:
                    login(request, student)
                    return HttpResponse("Now you're logged in")
                else:
                    return render(request, "registration/login_student.html", {
                    "form": form,
                    "error_message": "هذا الرقم غير مسجل، الرجاء التسجيل"
                    })




def logout_view(request):
    logout(request)
    return HttpResponse("You're logged out now")

def register_student(request):
    # if the request == GET then display the new registration form
    if request.method == "GET":
        return render(request, "registration/register_student.html", {
            "form": register_login_form(),
        })
    # if the request == POST then check the information 
    elif request.method == "POST":
        new_student = register_login_form(request.POST)
        if new_student.is_valid():
            phone_number = new_student.cleaned_data["phone_number"]

            # check if the phone number length is more than or equal to 10, if yes, then slice the last 9 numbers, if no send and error

            if len(phone_number) < 10:
                return render(request, "registration/register_student.html", {
                    "form": new_student,
                    "error_message": "الرجاء إدخال رقم التلفون بصورة صحيحة بهيئة 0912345678"
                })
            phone_number = f"249{phone_number[-9:]}"
            # try to save the new students to the database
            try:
                student = Student.objects.create_user(username=phone_number, password=USER_PASSWORD)
                student.save()
            except IntegrityError:
                return render(request, "registration/register_student.html", {
                    "form": new_student,
                    "error_message": " رقم التلفون موجود بالفعل إذهب صفحة تسجيل الدخول"
                })
            login(request, student)
            return HttpResponseRedirect(reverse("registration:index"))

            

def student_detail(request):
    pass

def register_for_program(request):
    pass