from django.contrib import admin
from .models import School,Teacher,AssignedTeacher,SchoolSessions,Student
# Register your models here.
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(AssignedTeacher)
admin.site.register(SchoolSessions)
admin.site.register(Student)
