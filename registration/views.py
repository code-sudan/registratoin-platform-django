# TODO: Localization to english and then Sudanese Arabic
# TODO: security for phone number and transaction ID


from urllib import response
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, request
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import CodeSudanQuote, Student, Registration
from .forms import *
from .sms import send_sms
from .utils import *
# import requests as req

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("registration:index"))

    if request.method == "GET":
        quote = get_quote()

        return render(request, "registration/login_student.html", {
            "form": register_login_form(),
            "progress": 0,
            "quote": quote,
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
                student = authenticate(
                    request, username=phone_number, password=pin)
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

    request.session["programs_count"] = Registration.objects.filter(
        student=request.user, is_enroll=False).count()
    return HttpResponseRedirect(reverse("registration:program_registration"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("registration:login"))


def register_student(request):
    # if the request == GET then display the new registration form

    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("registration:index"))
        else:
            quote = get_quote()
            return render(request, "registration/register_student.html", {
                "form": register_login_form(),
                "progress": 1,
                "quote": quote,
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
                    "error_message": "الرجاء إدخال معلومات صحيحة حسب وصف كل حقل",
                    "progress": 1,
                })
            if len(phone_number) < 10 or len(pin) != 1 or not pin.isnumeric():
                return render(request, "registration/register_student.html", {
                    "form": new_student,
                    "error_message": "الرجاء إدخال معلومات صحيحة حسب وصف كل حقل",
                    "progress": 1,
                })
            phone_number = f"249{phone_number[-9:]}"
            # try to save the new students to the database
            try:
                student = Student.objects.create_user(
                    username=phone_number, password=pin, is_complete=False)
                student.save()

            except Exception as e:
                print(e)
                return render(request, "registration/register_student.html", {
                    "form": new_student,
                    "error_message": " رقم التلفون موجود بالفعل إذهب لصفحة تسجيل الدخول"
                })
            login(request, student)

            # We're not sending SMS to the customer upon registration because there are some user who didn't finished their details, so we don't know 
            # Send the SMS to the customers when registered
            # send_sms(phone_number=phone_number, sms_to_send="registration_sms")

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
                Student.objects.filter(pk=request.user.pk).update(first_name=first_name, father_name=father_name, email=email, gender=gender,
                                                                  birthday=birthday, occupation=occupation, university=university, specialization=specialization, state=state, address=address)
                Student.objects.filter(pk=request.user.pk).update(is_complete=True)
            except:
                return render(request, "registration/student_details.html", {
                    "form": new_student_details,
                    "error_message": "للأسف واجهتنا مشكلة أثناء حفظ بياناتك الرجاء المحاولة مرة أخرى",
                })

            # sending the SMS when recieving the data
            # send_sms(phone_number=request.user.username, sms_to_send="details_completed", name=first_name)
            return HttpResponseRedirect(reverse("registration:program_registration"))
        else:
            return render(request, "registration/student_details.html", {
                "form": new_student_details,
                "error_message": "للأسف واجهتنا مشكلة أثناء حفظ بياناتك الرجاء المحاولة مرة أخرى",
            })


@login_required(redirect_field_name=None)
def program_registration(request):
    if request.method == "GET":
        
        quote = get_quote()


        return render(request, "registration/program_registration.html", {
            "form": new_program_form(),
            "progress": 40,
            "quote": quote,
        })
    elif request.method == "POST":
        new_registration = new_program_form(request.POST)
        if new_registration.is_valid():
            program = new_registration.cleaned_data["program"]
            try:
                registrated = Registration.objects.create(
                    student=request.user, program=program, is_register=True, is_enroll=False)

            except Exception as e:
                print(e)
                return render(request, "registration/program_registration.html", {
                    "form": new_registration,
                    "error_message": "هنالك مشكلة في البيانات التي قمت بإدخالها"
                })
            
            # send an SMS when the person registered for a program
            send_sms(request.user.username, sms_to_send="program_registration_sms", program=program.name_arabic)


            request.session["form_id"] = registrated.id
            request.session["programs_count"] = Registration.objects.filter(
                student=request.user, is_enroll=False).count()
            return render(request, f"registration/program_details.html", {
                "program_code": str(program.code),
                "program_name_arabic": str(program.name_arabic),
                "program_name_english": str(program.name_english),
                "track_name_arabic": str(program.track.name_arabic),
                "track_name_english": str(program.track.name_english),
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
            enrollment_form = Registration.objects.get(
                pk=request.session.get("form_id"))
        except:
            return HttpResponseRedirect(reverse("registration:program_registration"))
        if enrollment_form.is_register == False:
            return HttpResponseRedirect(reverse("registration:program_registration"))
        else:
            old_enrollment_form = new_enrollment_from()
            old_enrollment_form.initial["package"] = enrollment_form.package
            old_enrollment_form.initial["transaction_id"] = enrollment_form.transaction_id
            old_enrollment_form.initial["confirm_transaction"] = enrollment_form.transaction_id

            #get the quotation using get_quote function from the utils file
            quote = get_quote()

            return render(request, "registration/program_enrollment.html", {
                "form": old_enrollment_form,
                "progress": 80,
                "quote": quote,
            })

    elif request.method == "POST":
        new_enrollment = new_enrollment_from(request.POST)
        if new_enrollment.is_valid():
            transaction_id = int(new_enrollment.cleaned_data["transaction_id"])
            confirm_transaction = int(
                new_enrollment.cleaned_data["confirm_transaction"])
            package = new_enrollment.cleaned_data["package"]
            if transaction_id == confirm_transaction and transaction_id > 100000:
                try:
                    Registration.objects.filter(pk=request.session.get("form_id")).update(
                        transaction_id=transaction_id, package=package, is_enroll=True)
                    registration_form = Registration.objects.filter(
                        pk=request.session.get("form_id"))
                except:
                    return render(request, "registration/program_enrollment.html", {
                        "form": new_enrollment,
                        "progress": 60
                    })

                #send and SMS after enrollment
                send_sms(request.user.username, sms_to_send="program_enrollment_sms", program=registration_form[0].program.name_arabic)

                return render(request, "registration/successful.html", {
                    "progress": 100,
                })
            else:
                return render(request, "registration/program_enrollment.html", {
                    "error_message": "هنالك مشكلة في رقم العملية الذي أدخلته",
                    "form": new_enrollment,
                    "progress": 60
                })
        else:
            return render(request, "registration/program_enrollment.html", {
                "form": new_enrollment
            })


# Features


@login_required(redirect_field_name=None)
def my_programs(request):
    if request.method == "GET":
        all_programs = Registration.objects.filter(
            student=request.user, is_enroll=False).order_by("-created_at")
        return render(request, "registration/my_programs.html", {
            "all_programs": all_programs,
        })


@login_required(redirect_field_name=None)
def edit_form(request, operation, form_id):
    if operation == "edit":
        request.session["form_id"] = form_id
        return HttpResponseRedirect(reverse("registration:program_enrollment"))
    elif operation == "delete":
        Registration.objects.filter(pk=form_id).delete()
        request.session["programs_count"] = Registration.objects.filter(
            student=request.user, is_enroll=False).count()
        return HttpResponseRedirect(reverse("registration:my_programs"))


@login_required(redirect_field_name=None)
def send_sms_view(request):
    
    send_sms("249921093899", sms_to_send="details_completed", name="احمد")
    
    return HttpResponse("Hwlloe")


@staff_member_required
def registrations_list(request):
    if request.method == "GET":
        all_registrations = Registration.objects.all().order_by("-created_at")
        return render(request, "registration/registrations_list.html", {
            "all_registrations": all_registrations,
        })


@staff_member_required
def download_registration_csv(request):
    data = download_csv(request, Registration.objects.all())
    response = HttpResponse(data, content_type='text/csv; charset=utf-8-sig')
    return response