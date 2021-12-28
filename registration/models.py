from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Student(User):
    is_completed = models.BooleanField(null=False, default=False)

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

