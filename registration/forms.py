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
            "password": "إختار رقم واحد بين 0-9 لتسجيل الدخول بأمان في المستقبل"
        }
        widgets={
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control w-25 d-flex", "type": "number", "min": "0", "max": "9", "size": "20",})
        }
        required={
            "username",
            "password"
        }


class student_details_from(ModelForm):
    class Meta:
        model=Student

        SUDAN_STATES = [
            ("Outside Sudan", "خارج السودان"),
            ("Khartoum", "الخرطوم"),
            ("North Kordofan", "شمال كردفان"),
            ("Northern", "الشمالية"),
            ("Kassala", "كسّلا"),
            ("Blue Nile", "النيل الأزرق"),
            ("North Darfur", "شمال دارفور"),
            ("South Darfur", "جنوب دارفور"),
            ("South Kordofan", "جنوب كردفان"),
            ("Al Jazirah", "الجزيرة"),
            ("White Nile", "النيل الأبيض"),
            ("River Nile", "نهر النيل"),
            ("Red Sea", "البحر الأحمر"),
            ("Al Qadarif", "القضارف"),
            ("Sennar", "سنّار"),
            ("West Darfur", "غرب دارفور"),
            ("Central Darfur", "وسط دارفور"),
            ("East Darfur", "شرق دارفور"),
            ("East Darfur", "غرب كردفان"),
            ]
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
            "state": forms.Select(choices=SUDAN_STATES, attrs={"class": "form-select"}), 
            "address": forms.TextInput(attrs={"class": "form-control"}),

            

        }


class new_program_form(ModelForm):
    class Meta:
        model=Registration
        fields = ["program",]

        labels = {
            "program": "ما هو البرنامج الذي تريد التسجيل فيه",
        }

    
        widgets={
            "program": forms.Select(attrs={"class": "form-select"}),

        }
        required = (
            "program",
        )


class new_enrollment_from(ModelForm):
    confirm_transaction = forms.IntegerField(label="تأكيد رقم العملية", widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model=Registration
        fields = ["package", "transaction_id"]
        labels = {
            "transaction_id": "الرجاء إدخال رقم العملية:",
            "package": "ما هي النسخة التي تريد التسجيل فيها؟",
        }

        PACKAGES = [
            ("basic", "الأساسية"),
            ("golden", "الذهبية"),
        ]

        widgets = {
            "transaction_id": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "package": forms.Select(choices=PACKAGES, attrs={"class": "form-select"}),
        }
        
        required = (
            "package",
            "transaction_id"
        )


class first_lec_free_from(ModelForm):
    confirm_transaction = forms.IntegerField(label="تأكيد رقم العملية", widget=forms.TextInput(attrs={"class": "form-control"}))
    class Meta:
        model=Registration
        fields = ["package", "transaction_id"]
        labels = {
            "transaction_id": "الرجاء إدخال رقم العملية:",
            "package": "ما هي النسخة التي تريد التسجيل فيها؟",
        }

        PACKAGES = [
            ("basic", "الأساسية"),
            ("golden", "الذهبية"),
        ]

        widgets = {
            "transaction_id": forms.TextInput(attrs={"class": "form-control", "type": "number"}),
            "package": forms.Select(choices=PACKAGES, attrs={"class": "form-select"}),
        }
        
        required = (
            "package",
            "transaction_id"
        )



