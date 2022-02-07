from django.contrib import admin
from .models import *

# Register your models here.

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'program', 'created_at', 'package', 'is_enroll', 'transaction_id')
    list_filter = ('created_at', 'is_enroll', 'program')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'email', 'is_complete')


admin.site.register(Student, StudentAdmin)
admin.site.register(Track)
admin.site.register(Program)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Batch)

