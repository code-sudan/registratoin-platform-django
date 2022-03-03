from django.contrib import admin
from .models import *

# Register your models here.

def get_phone_number(obj):
    return(f"{obj.student.username}")
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', get_phone_number, 'program', 'created_at', 'package', 'is_enroll', 'transaction_id')
    list_filter = ('created_at', 'is_enroll', 'program')

def full_name(obj):
    return(f"{obj.first_name} {obj.father_name}")
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', full_name, 'email', 'university', 'is_complete')
 

admin.site.register(Student, StudentAdmin)
admin.site.register(Track)
admin.site.register(Program)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Batch)
admin.site.register(CodeSudanQuote)
