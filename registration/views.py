from django.shortcuts import render
from .models import Register, User
from django import forms

# Create your views here.
from django.http import HttpResponse
from secrets import randbelow

# Create your views here.



from django.contrib.auth.backends import BaseBackend
class PhoneModelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        kwargs = {'phone': username}

def index(request):
    return HttpResponse("Hello, world!")



class new_signup(forms.Form):
    phone_number = forms.CharField(max_length=12, label="رقم تلفونك")

def signup(request):
    if request.method == "GET":
        return render(request, "registration/signup.html", {
            "form": new_signup()
        })

    elif request.method == "POST":
        form = new_signup(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            pin = randbelow(10)

            new_user = User.objects.create_user(USERNAME_FIELD=phone_number, pin = pin)
            new_user.save()
            return HttpResponse(f"رقمك السري الجديد هو {pin} الرجاء المحافظة عليه لتسجيل الدخول كل مرة")
        else:
            return render(request, "registration/signup.html", {
                "form": form
            })
    


class new_register(forms.Form):
    register_email = forms.EmailField(label="البريد الإلكتروني")
    register_name = forms.CharField(label="الإسم كاملا ", max_length=64)
    program = forms.CharField(label="ما هو البرنامج الذي إخترته؟ ", max_length=64)

def register(request):
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