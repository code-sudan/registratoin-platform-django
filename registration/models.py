from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.
class Student(AbstractUser):
    GENDER_CHOICE = (("M", 'ذكر'), ("F", "أنثى"),)
    SUDAN_STATES = [("الخرطوم"), ("الشمالية")]

    is_complete = models.BooleanField(null=False, default=False)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    father_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=64, blank=True, null=True)
    university = models.CharField(max_length=64, blank=True, null=True)
    specialization = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64 ,blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return(f"{self.first_name} {self.father_name}")



class Track(models.Model):
    id = models.AutoField(primary_key=True)
    name_english = models.CharField(max_length=64, null = False)
    name_arabic = models.CharField(max_length=64, null = False)

    def __str__(self):
        return(self.name_english)

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    name_english = models.CharField(max_length=64, null=False)
    name_arabic = models.CharField(max_length=64, null = False)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)

    def __str__(self):
        return(self.name_arabic)

class Batch(models.Model):
    id=models.AutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    number = models.IntegerField()
    started_at = models.DateField()

    def __str__(self):
        return (f"{self.number}")


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    package = models.CharField(max_length=64)
    is_register = models.BooleanField(default=False)
    transaction_id = models.PositiveBigIntegerField(null=True, default=None)
    is_enroll = models.BooleanField(default=False)

    def __str__(self):
        return(f"{self.student.first_name} PN {self.student.username} registerd for {self.program} is_enroll {self.is_enroll}")


class CodeSudanQuote(models.Model):
    id = models.AutoField(primary_key=True)
    quote = models.TextField()
    by = models.CharField(max_length=64)
    
    def __str__(self):
        return(f"{self.quote[:40]}: {self.by}")
