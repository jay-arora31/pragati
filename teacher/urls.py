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
            path('add_student_excel/',views.add_student_excel,name='add_student_excel' ),
            path('view_student/',views.view_student,name='view_student' ),
            path('filter_class_subject/',views.filter_class_subject,name='filter_class_subject' ),
            path('add_test/',views.add_test,name='add_test' ),
            path('view_all_test/',views.view_all_test,name='view_all_test' ),
            path('select_test_outcome/',views.select_test_outcome,name='select_test_outcome' ),
            path('add_question_outcome/',views.add_question_outcome,name='add_question_outcome' ),
            path('select_subject_test/',views.select_subject_test,name='select_subject_test' ),
            path('add_student_marks/',views.add_student_marks,name='add_student_marks' ),
            path('filter_class_subject1/',views.filter_class_subject1,name='filter_class_subject1' ),
            path('add_student_filter_class_subject/',views.add_student_filter_class_subject,name='add_student_filter_class_subject' ),
            path('filter_student_marks_outcomes1/',views.filter_student_marks_outcomes1,name='filter_student_marks_outcomes1' ),
            path('add_marks_excel/',views.add_marks_excel,name='add_marks_excel' ),
            path('select_sport/',views.select_sport,name='select_sport' ),
            path('sport_filter_session/',views.sport_filter_session,name='sport_filter_session' ),
            path('sport_filter_roll/',views.sport_filter_roll,name='sport_filter_roll' ),
            path('view_sport/',views.view_sport,name='view_sport' ),
            path('testing_function/',views.testing_function,name='testing_function' ),
            path('testing_function_login/',views.testing_function_login,name='testing_function_login' ),
            path('teacher_select_wise_subject/',views.teacher_select_wise_subject,name='teacher_select_wise_subject' ),
            path('add_subject_outcome/',views.add_subject_outcome,name='add_subject_outcome' ),
            path('class_subject_test/',views.class_subject_test,name='class_subject_test' ),
            path('add_test_next/',views.add_test_next,name='add_test_next' ),
            path('select_cultural/',views.select_cultural,name='select_cultural' ),




]
