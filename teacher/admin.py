from django.contrib import admin
from .models import AddTest,AssignOutcome,TestMark,Sports,AcademicCount
# Register your models here.
admin.site.register(AddTest)
admin.site.register(AssignOutcome)
admin.site.register(TestMark)
admin.site.register(Sports)
admin.site.register(AcademicCount)
