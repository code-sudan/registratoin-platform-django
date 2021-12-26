from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Register(models.Model):
    register_id = models.IntegerField()
    register_email = models.EmailField()
    register_name = models.CharField(max_length=64)
    program = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.register_name} choice {self.program}"

class User(AbstractUser):
    pass
