from importlib.metadata import requires
from tkinter.constants import CASCADE

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Users(models.Model):
    user_name = models.CharField(max_length=25 , unique=True)
    password = models.CharField(max_length=128)


class Task(models.Model):
    task = models.TextField(max_length=200)
    status = models.BooleanField(default=False)
    user_name = models.ForeignKey(
        Users,
        to_field='user_name',
        on_delete=models.CASCADE
    )