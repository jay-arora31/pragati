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
      path('assign_teacher/',views.assign_teacher,name='assign_teacher' ),
      #path('add_student/',views.add_student,name='add_student' ),
      path('teacher_view/',views.teacher_view,name='teacher_view' ),
      path('teacher_delete/<int:id>',views.teacher_delete,name='teacher_delete' ),
      path('select_student/',views.select_student,name='select_student' ),
      #path('add_marks/',views.add_marks,name='add_marks' ),
      path('submit_marks/',views.submit_marks,name='submit_marks' ),
      path('assign_subject/',views.assign_subject,name='assign_subject' ),
      path('view_subjects/',views.view_subjects,name='view_subjects' ),
      path('view_class_subjects/<str:key>/',views.view_class_subjects,name='view_class_subjects' ),
        path('get-topics-ajax/', views.get_topics_ajax, name="get_topics_ajax"),
      path('subject_delete/<int:id>/',views.subject_delete,name='subject_delete' ),
      path('view_assigned_teachers/',views.view_assigned_teachers,name='view_assigned_teachers' ),
      path('assign_sport_teacher/',views.assign_sport_teacher,name='assign_sport_teacher' ),
      path('assign_cultural_teacher/',views.assign_cultural_teacher,name='assign_cultural_teacher' ),
      path('student_register/',views.student_register,name='student_register' ),
      path('view_sports_teacher/',views.view_sports_teacher,name='view_sports_teacher' ),
      path('class_wise_subject/',views.class_wise_subject,name='class_wise_subject' ),
      path('teacher_namewise_email/',views.teacher_namewise_email,name='teacher_namewise_email' ),

      

]
