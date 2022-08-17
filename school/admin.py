from django.contrib import admin
from .models import School,Teacher,AssignedTeacher,SchoolSessions,Student,StudentMarks,class_subject,AssignSportTeacher
from teacher.models import *

# Register your models here.
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(AssignedTeacher)
admin.site.register(SchoolSessions)
admin.site.register(Student)
admin.site.register(StudentMarks)
admin.site.register(class_subject)
admin.site.register(AssignSportTeacher)
