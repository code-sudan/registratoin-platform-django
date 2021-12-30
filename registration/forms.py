from django.db.models.base import Model
from django.forms import ModelForm, fields, widgets
from .models import Student
from django import forms


# registration and login form
class register_login_form(ModelForm):
    class Meta:
        model=Student
        fields=["username"]
        labels={
            "username": "رقم التلفون"
        }
        help_texts={
            "username": "الرجاء إدخال رقم تلفونك المكون من 10 أرقام"
        }
        widgets={
            "username": forms.TextInput(attrs={"class": "form-control"})
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
        )
        widgets = {
            
            "first_name": forms.TextInput(attrs={"class": "form-control mb-2", "required": True}),
            "father_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "required": True}),
            "gender": forms.Select(attrs={"class": "form-select", "required": True}),
            "birthday": forms.SelectDateWidget(
                months = {
                    1:('يناير'), 2:('فبراير'), 3:('مارس'), 4:('أبريل'),
                    5:('مايو'), 6:('يونيو'), 7:('يوليو'), 8:('أغسطس'),
                    9:('سبتمبر'), 10:('أكتوير'), 11:('نوفمبر'), 12:('ديسمبر')
                    }, 
                attrs={"class": "form-control", "required": True}
            ),
            "occupation": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "university": forms.TextInput(attrs={"class": "form-control", "required": True}), 
            "specialization": forms.TextInput(attrs={"class": "form-control", "required": True}), 
            "state": forms.TextInput(attrs={"class": "form-control", "required": True}), 
            "address": forms.TextInput(attrs={"class": "form-select"}),

            

        }


