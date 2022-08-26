





from msilib.schema import Class

from django import forms
from .models import *
from school.models import *
from teacher.models import *

from django import forms



class AddTestForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AddTestForm,self).__init__(*args,**kwargs)
        self.fields['test_name'].widget.attrs['class'] = 'form-control form-group'
        self.fields['test_class'].widget.attrs['class'] = 'form-control form-group'
        self.fields['no_que'].widget.attrs['class'] = 'form-control form-group'
    class Meta:
                model =AddTest
                fields =('test_name','test_class','no_que')
                widgets = {
     

                    }
                labels = {
                            
                             'test_name': ('Test Name'),
                             'no_que': ('Number of question'),
                }    
