from msilib.schema import Class
from django.forms import ModelForm

from django import forms
from datetime import datetime
from .models import *
from school.models import *
from django.contrib.auth.forms import UserCreationForm,UserChangeForm ,PasswordChangeForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row, Column, Submit
from django.contrib.auth.forms import AuthenticationForm
class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model =CustomUser
        fields =['email']


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')
        self.fields['password1'].help_text =""
        self.fields['email'].help_text =""
    
        self.fields['email'].widget.attrs['class'] = 'form-control'

        self.helper = FormHelper()
        self.helper.layout=Layout(
            
            'email',
            'password1',
            Submit('submit', 'Sign up')
        )
class CustomUserCreationForm1(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model =CustomUser
        fields =['email']


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')
        self.fields['password1'].help_text =""
        #self.fields['username'].help_text=""
        self.fields['password1'].widget.attrs.update(style='max-height: 33px')
        #self.fields['username'].widget.attrs.update(style='max-height: 33px')
        self.fields['email'].widget.attrs.update(style='max-height: 33px')
        #self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'

        self.helper = FormHelper()
        self.helper.layout=Layout(
            
            'email',
            'password1',
            Submit('submit', 'Sign up')
        )
class School_info(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(School_info,self).__init__(*args,**kwargs)


    class Meta:
            model =School
            fields =('s_name',)
            widgets = {
                    's_name': forms.TextInput(attrs={'class': 'name'}),
                }
            labels = {
                        's_name': ('School Name'),
             
                    }


class add_subject_gov(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(add_subject_gov,self).__init__(*args,**kwargs)

        self.fields['subject_name'].widget.attrs['class'] = 'form-control'
        self.fields['subject_class'].widget.attrs['class'] = 'form-control'

    class Meta:
            model =GovtSubject
            fields =('subject_class','subject_name')
            widgets = {
                    
                }
            labels = {
                        'subject_name': ('Subject Name'),
                        'subject_class': ('Subject Class'),
             
                    }



class Teacher_info(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(Teacher_info,self).__init__(*args,**kwargs)
        self.fields['t_name'].widget.attrs['class'] = 'form-control'
 
    class Meta:
                model =Teacher
                fields =('t_name',)
                widgets = {
                        't_name': forms.TextInput(attrs={'class': 'name'}),
                    }
                labels = {
                            't_name': ('Teachers Name'),
                }

