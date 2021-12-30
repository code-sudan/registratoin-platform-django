from django.contrib import admin
from .models import Student, Track, Program, Registration

# Register your models here.

admin.site.register(Student)
admin.site.register(Track)
admin.site.register(Program)
admin.site.register(Registration)
