from django.db import models

from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django.forms import ModelForm
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings





class CustomUser(AbstractUser):
    email =models.EmailField(unique =True)
    name =models.CharField(max_length =255, null=True,blank=True)

    is_school = models.BooleanField(default = False)
    is_govt = models.BooleanField(default = False)
    is_teacher = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    is_active =models.BooleanField(default=True) 



