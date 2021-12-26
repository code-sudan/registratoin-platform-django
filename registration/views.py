from django.shortcuts import render
from django.urls import reverse
from .models import Register
from django import forms

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from secrets import randbelow
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


USER_PASSWORD = "codesudan"


# Create your views here.

@login_required
def index(request):
    return HttpResponse("Hello, world!")

class new_user_form(forms.Form):
    phone_number = forms.CharField(max_length=12, label="رقم تلفونك")

def user_reg(request):
    if request.method == "GET":
        return render(request, "registration/user_reg.html", {
            "form": new_user_form()
        })
    elif request.method == "POST":
        form = new_user_form(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            try:
                user=User.objects.create_user(username=phone_number, password=USER_PASSWORD)
                user.save()
            except IntegrityError:
                return render(request, "registration/user_reg.html", {
                    "form": form,
                    "message": "المستخدم موجود لدينا"
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "registration/user_reg.html", {
            "form": new_user_form()
            })

def user_logout(request):
    logout(request)
    return HttpResponse("you're logged out")




class new_register(forms.Form):
    register_email = forms.EmailField(label="البريد الإلكتروني")
    register_name = forms.CharField(label="الإسم كاملا ", max_length=64)
    program = forms.CharField(label="ما هو البرنامج الذي إخترته؟ ", max_length=64)

def program_reg(request):
    if request.method == "GET":
        return render(request, "registration/register.html", {
            "form": new_register()
        })
    elif request.method == "POST":
        form = new_register(request.POST)

        if form.is_valid():
            register_name = form.cleaned_data["register_name"]
            register_email = form.cleaned_data["register_email"]
            program = form.cleaned_data["program"]
            new_registeration = Register(register_id=0, register_name=register_name, register_email=register_email, program=program)
            new_registeration.save()
            return HttpResponse("it's been save to the database successfully")