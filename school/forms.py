


from msilib.schema import Class

from django import forms
from .models import *
from school.models import *
from teacher.models import *

from django import forms



class AssignCourseTeacher(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AssignCourseTeacher,self).__init__(*args,**kwargs)
        self.fields['course_class'].widget.attrs['class'] = 'form-control form-group'
        self.fields['course_class'].widget.attrs['placeholder'] = 'form-control form-group'
    class Meta:
                model =AssignedTeacher
                fields =('course_class',)
                widgets = {
     

                    }
                labels = {
                            
                             'course_class': ('Course Class'),
                }    


class AddStudentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AddStudentForm,self).__init__(*args,**kwargs)
        self.fields['student_name'].widget.attrs['class'] = 'form-control'
        self.fields['student_roll'].widget.attrs['class'] = 'form-control'

 
    class Meta:
                model =Student
                fields =('student_roll','student_name')
                
                labels = {
                            'student_roll': ('Student Roll Number'),
                            'student_name': ('Student Name'),
                }





class AddMarks(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AddMarks,self).__init__(*args,**kwargs)
        self.fields['eng'].widget.attrs['class'] = 'form-control'

 
    class Meta:
                model =StudentMarks
                fields =('eng','hindi','math','sst','sci')
                
                labels = {
                            'eng': ('English'),
                            'hindi': ('Hindi'),
                            'math': ('Maths'),
                            'sst': ('Social studies'),
                            'sci': ('Science'),
                }





class AssignClassCourse(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(AssignClassCourse,self).__init__(*args,**kwargs)
        self.fields['subject_name'].widget.attrs['class'] = 'form-control form-group'
        self.fields['subject_learning'].widget.attrs['class'] = 'form-control form-group'
        self.fields['subject_class'].widget.attrs['class'] = 'form-control form-group'
    class Meta:
                model =class_subject
                fields =('subject_name','subject_class','subject_learning')
                widgets = {
     

                    }
                labels = {
                            
                             'subject_name': ('Subject Name'),
                             'subject_class': ('Subject Class'),
                             'subject_learning': ('Subject Learning Outcome'),
                }    

