from django.contrib import admin
from .models import CustomUser,GovtSubject,GovtAssignOutcome


# Register your models here.
admin.site.register(CustomUser)                                   #registering the User in Admin
admin.site.register(GovtSubject)                                   #registering the User in Admin
admin.site.register(GovtAssignOutcome)                                   #registering the User in Admin
