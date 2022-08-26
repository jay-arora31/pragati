from django.db import models

from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django.forms import ModelForm
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


CLASS_CHOICES= [
        ('1', '1'),
        ('2', '2'),
       

        ]


class CustomUser(AbstractUser):
    email =models.EmailField(unique =True)
    name =models.CharField(max_length =255, null=True,blank=True)

    is_school = models.BooleanField(default = False)
    is_govt = models.BooleanField(default = False)
    is_teacher = models.BooleanField(default = False)
    is_student = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    is_active =models.BooleanField(default=True) 



class GovtSubject(models.Model): 
    subject_name=models.CharField(max_length =255, null=True,blank=True)
    subject_class=models.CharField(max_length =255, null=True,blank=True,choices=CLASS_CHOICES)
    subject_learning=models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.subject_name

class GovtAssignOutcome(models.Model):
    ot_no=models.CharField(max_length =255, null=True,blank=True)
    ot_name=models.CharField(max_length =255, null=True,blank=True)
    ot_class=models.ForeignKey( GovtSubject, on_delete=models.CASCADE)

    def __str__(self):
        return self.ot_name
