from django.contrib import admin
from .models import School,StudentAccount,Teacher,AssignedTeacher,SchoolSessions,Student,StudentMarks,class_subject,AssignSportTeacher
from teacher.models import *
from .models import school_class_subject,SchoolAssignedTeacher
# Register your models here.
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(AssignedTeacher)
admin.site.register(SchoolSessions)
admin.site.register(Student)
admin.site.register(StudentMarks)
admin.site.register(class_subject)
admin.site.register(AssignSportTeacher)
admin.site.register(StudentAccount)
admin.site.register(school_class_subject)
admin.site.register(SchoolAssignedTeacher)
