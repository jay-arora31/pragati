from ast import Assign
from msilib.schema import Class
from statistics import mode
from django.db import models
from django.conf import settings

# Create your models here.

COURSE_CHOICES= [
        ('English', 'English'),
        ('Maths', 'Maths'),

        ]
CLASS_CHOICES= [
        ('1', 'Standard 1'),
        ('2', 'Standard 2'),
        ('3', 'Standard 3'),
        ('4', 'Standard 4'),

        ]
class School(models.Model):
    s_name =models.CharField(max_length =255, null=True,blank=True)
    s_district =models.CharField(max_length =255, null=True,blank=True)
    s_city =models.CharField(max_length =255, null=True,blank=True)
    s_city =models.CharField(max_length =255, null=True,blank=True)
    s_info= models.ForeignKey(settings.AUTH_USER_MODEL,db_index=True,on_delete =models.CASCADE)
    def __str__(self):
        return self.s_name

class Teacher(models.Model):
    t_name=models.CharField(max_length =255, null=True,blank=True)
    t_school =models.ForeignKey( School,on_delete=models.CASCADE)
    t_info= models.ForeignKey(settings.AUTH_USER_MODEL,db_index=True,on_delete =models.CASCADE)
    def __str__(self):
        return self.t_name
'''
class Classes(models.Model):
    c_standard=models.CharField(max_length =255, null=True,blank=True)
    c_school =models.ForeignKey( School,related_name='school_info',on_delete=models.CASCADE)
    c_teacher =models.ForeignKey( Teacher,related_name='teacher_info',on_delete=models.CASCADE)
'''

class Student(models.Model):
    student_name=models.CharField(max_length =255, null=True,blank=True)
    student_course_name=models.CharField(max_length =255, null=True,blank=True)
    student_school =models.ForeignKey( School, on_delete=models.CASCADE)
    student_teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    student_class=models.CharField(max_length =255, null=True,blank=True)
    def __str__(self):
        return self.student_name


class AssignedTeacher(models.Model):
    course_name=models.CharField(max_length =255, null=True,blank=True,choices=COURSE_CHOICES)
    course_class=models.CharField(max_length =255,null=True,blank=True,choices=CLASS_CHOICES)
    course_teacher=models.ForeignKey( Teacher, on_delete=models.CASCADE)
    course_school=models.ForeignKey( School, on_delete=models.CASCADE)
    def __str__(self):
        return self.course_name


