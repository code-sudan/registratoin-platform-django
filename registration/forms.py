from django.db.models.base import Model
from django.forms import ModelForm, fields, widgets
from .models import Registration, Student
from django import forms


# registration and login form
class register_login_form(ModelForm):
    class Meta:
        model=Student
        fields=["username", "password"]
        labels={
            "username": "رقم التلفون",
            "password": "رقم الأمان",
        }
        help_texts={
            "username": "الرجاء إدخال رقم تلفونك المكون من 10 أرقام",
            "password": "إختار رقم بين 0-9 لتسجيل الدخول بأمان في المستقبل"
        }
        widgets={
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "type": "number", "min": "0", "max": "9", })
        }
        required={
            "username",
            "password"
        }


class student_details_from(ModelForm):
    class Meta:
        model=Student
        fields=["first_name", "father_name", "email", "gender", "birthday", "occupation", "university", "specialization", "state", "address"]
        labels = {
            "first_name": "إسمك",
            "father_name":"إسم الوالد",
            "email":"بريدك الإلكتروني",
            "gender": "النوع",
            "birthday":"تاريخ ميلادك",
            "occupation":"المهنة",
            "university":"الجامعة",
            "specialization":"التخصص",
            "state":"الولاية",
            "address":"العنوان",
        }
        required = (
            "first_name",
            "father_name",
            "email",
            "gender",
            "birthday",
            "occupation",
            "university",
            "specialization",
            "state",
        )
        widgets = {
            
            "first_name": forms.TextInput(attrs={"class": "form-control mb-2", "required": True}),
            "father_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "required": True}),
            "gender": forms.Select(attrs={"class": "form-select", "required": True}),
            "birthday": forms.DateInput(attrs={"type": "date"}),
            "occupation": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "university": forms.TextInput(attrs={"class": "form-control", "required": True}), 
            "specialization": forms.TextInput(attrs={"class": "form-control", "required": True}), 
            "state": forms.TextInput(attrs={"class": "form-control", "required": True}), 
            "address": forms.TextInput(attrs={"class": "form-select"}),

            

        }


class new_program_form(ModelForm):
    class Meta:
        model=Registration
        fields = ["program", "package", "batch"]

        labels = {
            "program": "ما هو البرنامج الذي تريد التسجيل فيه",
            "package": "ما هي النسخة التي تريد التسجيل فيها؟",
            "batch": "ما هي الدفعة التي تريد الانضمام لها؟"
        }

        PACKAGES = [
            ("basic", "الأساسية"),
            ("golden", "الذهبية"),
        ]
        widgets={
            "program": forms.Select(attrs={"class": "form-select"}),
            "package": forms.Select(choices=PACKAGES, attrs={"class": "form-select"}),
            "batch": forms.Select(attrs={"class": "form-select"})

        }
        required = (
            "program",
            "package",
            "batch"
        )


class new_enrollment_from(ModelForm):
    confirm_transaction = forms.IntegerField(label="تأكيد رقم العملية", widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model=Registration
        fields = ["transaction_id"]
        labels = {
            "transaction_id": "الرجاء إدخال رقم العملية:",
        }

        widgets = {
            "transaction_id": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
        }




