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



class Track(models.Model):
    id = models.AutoField(primary_key=True)
    name_english = models.CharField(max_length=64, null = False, default="old")
    name_arabic = models.CharField(max_length=64, null = False, default="قديم")

    def __str__(self):
        return(self.name_english)

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    name_english = models.CharField(max_length=64, null=False, default="old")
    name_arabic = models.CharField(max_length=64, null = False, default="قديم")
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self):
        return(self.name_english)

