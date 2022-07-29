


from msilib.schema import Class

from django import forms
from .models import *
from school.models import *

from django import forms



class AssignCourseTeacher(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AssignCourseTeacher,self).__init__(*args,**kwargs)
        self.fields['course_name'].widget.attrs['class'] = 'form-select form-select-lg mb-3'
        self.fields['course_class'].widget.attrs['class'] = 'form-select form-select-lg mb-3'
    class Meta:
                model =AssignedTeacher
                fields =('course_name','course_class')
                widgets = {
     

                    }
                labels = {
                            'course_name': ('Course Name'),
                             'course_class': ('Course Class'),
                }    


class AddStudentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AddStudentForm,self).__init__(*args,**kwargs)
        self.fields['student_name'].widget.attrs['class'] = 'form-control'

 
    class Meta:
                model =Student
                fields =('student_name',)
                widgets = {
                        'student_name': forms.TextInput(attrs={'class': 'name'}),
                    }
                labels = {
                            'student_name': ('Student Name'),
                }







