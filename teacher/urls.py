"""pragati URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from . import views


urlpatterns = [
    
     
            #path('add_marks/',views.add_marks,name='add_marks' ),
            path('add_student/',views.add_student,name='add_student' ),
            path('filter_class_subject/',views.filter_class_subject,name='filter_class_subject' ),
            path('add_test/',views.add_test,name='add_test' ),
            path('view_all_test/',views.view_all_test,name='view_all_test' ),
            path('select_test_outcome/',views.select_test_outcome,name='select_test_outcome' ),
            path('add_question_outcome/',views.add_question_outcome,name='add_question_outcome' ),


]