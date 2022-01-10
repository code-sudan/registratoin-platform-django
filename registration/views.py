from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, request
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Registration
from .forms import *

# Create your views here.


def login_view(request):
    if request.method == "GET":
        return render(request, "registration/login_student.html", {
            "form": register_login_form(),
            "progress": 0,
        })
    elif request.method == "POST":
        form = register_login_form(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["username"]
            pin = form.cleaned_data["password"]
            phone_number = f"249{phone_number[-9:]}"
            if len(phone_number) < 10 or len(pin) != 1 or not pin.isnumeric():
                return render(request, "registration/login_student.html", {
                    "form": form,
                    "error_message": "الرجاء إدخال معلومات صحيحة حسب وصف كل حقل"
                })
            else:
                student = authenticate(request, username=phone_number, password=pin)
                if student is not None:
                    login(request, student)
                    return HttpResponseRedirect(reverse("registration:index"))
                else:
                    return render(request, "registration/login_student.html", {
                    "form": form,
                    "error_message": "هذا الرقم غير مسجل، الرجاء التسجيل"
                    })
        else:
            return render(request, "registration/login_student.html", {
                "form": form,
                "error_message": "الرجاء المحاولة مرة أخرى"
                })

@login_required(redirect_field_name=None)
def index(request):
    if not request.user.is_complete:
        return HttpResponseRedirect(reverse("registration:student_details")) 
    return HttpResponseRedirect(reverse("registration:program_registration"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("registration:login"))

def register_student(request):
    # if the request == GET then display the new registration form
    
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "registration/register_student.html", {
            "error_message": "أنت مسجل وأتممت عملية الدخول",
            })
        else:
            return render(request, "registration/register_student.html", {
            "form": register_login_form(),
            "progress": 0,
            })
    # if the request == POST then check the information 
    elif request.method == "POST":
        new_student = register_login_form(request.POST)
        if new_student.is_valid():
            phone_number = new_student.cleaned_data["username"]
            pin = new_student.cleaned_data["password"]

            # check if the phone number length is more than or equal to 10, if yes, then slice the last 9 numbers, if no send and error
            # check if the pin number isn't numaric or isn't a one number.
            if len(pin) != 1 or not pin.isnumeric():
                return render(request, "registration/register_student.html", {
                    "form": new_student,
                    "error_message": "الرجاء إدخال معلومات صحيحة حسب وصف كل حقل"
                })
            if len(phone_number) < 10 or len(pin) != 1 or not pin.isnumeric():
                return render(request, "registration/register_student.html", {
                    "form": new_student,
                    "error_message": "الرجاء إدخال معلومات صحيحة حسب وصف كل حقل"
                })
            phone_number = f"249{phone_number[-9:]}"
            # try to save the new students to the database
            try:
                student = Student.objects.create_user(username=phone_number, password=pin, is_complete = False)
                student.save()
            except Exception as e:
                print(e)
                return render(request, "registration/register_student.html", {
                    "form": new_student,
                    "error_message": " رقم التلفون موجود بالفعل إذهب صفحة تسجيل الدخول"
                })
            login(request, student)
            return HttpResponseRedirect(reverse("registration:index"))
        else:
            return render(request, "registration/register_student.html", {
            "form": new_student,
            })

@login_required(redirect_field_name=None)
def student_details(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            student_details_form = student_details_from()
            
            user_details = Student.objects.filter(pk=request.user.id)

            student_details_form.initial["first_name"] = user_details[0].first_name
            student_details_form.initial["father_name"] = user_details[0].father_name
            student_details_form.initial["email"] = user_details[0].email
            student_details_form.initial["gender"] = user_details[0].gender
            student_details_form.initial["birthday"] = user_details[0].birthday
            student_details_form.initial["occupation"] = user_details[0].occupation
            student_details_form.initial["university"] = user_details[0].university
            student_details_form.initial["specialization"] = user_details[0].specialization
            student_details_form.initial["state"] = user_details[0].state
            student_details_form.initial["address"] = user_details[0].address

            return render(request, "registration/student_details.html", {
                "form": student_details_form,
            })

        else:
            return render(request, "registration/student_details.html", {
                "form": student_details_from(),
                "progress": 20,
            })
    elif request.method == "POST":
        new_student_details = student_details_from(request.POST)
        if new_student_details.is_valid():
            first_name = new_student_details.cleaned_data["first_name"]
            father_name = new_student_details.cleaned_data["father_name"]
            email = new_student_details.cleaned_data["email"]
            gender = new_student_details.cleaned_data["gender"]
            birthday = new_student_details.cleaned_data["birthday"]
            occupation = new_student_details.cleaned_data["occupation"]
            university = new_student_details.cleaned_data["university"]
            specialization = new_student_details.cleaned_data["specialization"]
            state = new_student_details.cleaned_data["state"]
            address = new_student_details.cleaned_data["address"]

            try:
                Student.objects.filter(pk=request.user.pk).update(first_name = first_name, father_name=father_name, email=email, gender = gender, birthday=birthday, occupation=occupation, university=university, specialization=specialization, state=state, address=address)
                Student.objects.filter(pk=request.user.pk).update(is_complete=True)
            except:
                return render(request, "registration/student_details.html",{
                "form": new_student_details,
                "error_message": "للأسف واجهتنا مشكلة أثناء حفظ بياناتك الرجاء المحاولة مرة أخرى",
                })
            
            return HttpResponseRedirect(reverse("registration:program_registration"))
        else:
            return render(request, "registration/student_details.html",{
                "form": new_student_details,
                "error_message": "للأسف واجهتنا مشكلة أثناء حفظ بياناتك الرجاء المحاولة مرة أخرى",
            })

@login_required(redirect_field_name=None)
def program_registration(request):
    if request.method == "GET":
        return render(request, "registration/program_registration.html", {
            "form": new_program_form(),
            "progress": 40,
        })
    elif request.method == "POST":
        new_registration = new_program_form(request.POST)
        if new_registration.is_valid():
            program = new_registration.cleaned_data["program"]
            package = new_registration.cleaned_data["package"]
            batch = new_registration.cleaned_data["batch"]
            try:
                registrated = Registration.objects.create(student=request.user, program=program, package=package, batch=batch, is_register=True, is_enroll = False)
            except:
                 return render(request, "registration/program_registration.html", {
                "form": new_registration,
                "error_message": "هنالك مشكلة في البيانات التي قمت بإدخالها"
                })
            request.session["form_id"] = registrated.id
            return render(request, f"registration/program_details.html", {
                "package": package, 
                "program_code": str(program.code),
                "program_name_arabic": str(program.name_arabic),
                "program_name_english": str(program.name_english),
                "track_name_arabic": str(program.track.name_arabic),
                "track_name_english": str(program.track.name_english),
                "batch": str(batch.started_at),
                "progress": 40,
            })

        else:
            return render(request, "registration/program_registration.html", {
                "form": new_registration,
                "error_message": "الرجاء المحاولة مرة أخرى"
            })

@login_required(redirect_field_name=None)
def program_enrollment(request):
    if request.method == "GET":
        try: 
            enrollment_form = Registration.objects.get(pk=request.session.get("form_id"))
        except:
            return HttpResponseRedirect(reverse("registration:program_registration"))
        if enrollment_form.is_register == False:
            return HttpResponseRedirect(reverse("registration:program_registration"))
        elif enrollment_form.is_enroll == True:
            return HttpResponseRedirect(reverse("registration:index"))
        else:
            return render(request, "registration/program_enrollment.html", {
                "form": new_enrollment_from(),
                "progress": 60,
            })
        
    elif request.method == "POST":
        new_enrollment = new_enrollment_from(request.POST)
        if new_enrollment.is_valid():
            transaction_id = new_enrollment.cleaned_data["transaction_id"]
            try:
                Registration.objects.filter(pk=request.session.get("form_id")).update(transaction_id = transaction_id, is_enroll = True)
            except:
                return render(request, "registration/program_enrollment.html", {
                "form": new_enrollment
                })
            return HttpResponse(f"you transaction id is {transaction_id}")
            
        else:
            return render(request, "registration/program_enrollment.html", {
            "form": new_enrollment
            })
        
