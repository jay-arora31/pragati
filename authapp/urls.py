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
      path('home/',views.home,name='home' ),
      path('school_home/',views.school_home,name='school_home' ),
      path('govt_home/',views.govt_home,name='govt_home' ),
      path('teacher_home/',views.teacher_home,name='teacher_home' ),
      path('student_home/',views.student_home,name='student_home' ),
      path('school_view/',views.school_view,name='school_view' ),
      path('school_active/<str:email>',views.school_active,name='school_active' ),
      path('school_inactive/<str:email>',views.school_inactive,name='school_inactive' ),
      path('school_delete/<str:email>',views.school_delete,name='school_delete' ),

      
      path('register_school/',views.register_school,name='register_school' ),
      path('register_teacher/',views.register_teacher,name='register_teacher' ),

      path('',views.login,name='login' ),
      path('logout/',views.logout,name='logout_view' ),
















      path('gov_add_subject/',views.gov_add_subject,name='gov_add_subject' ),
      path('gov_view_subject/',views.gov_view_subject,name='gov_view_subject' ),
      path('gov_view_subject_delete/<int:id>',views.gov_view_subject_delete,name='gov_view_subject_delete' ),

      

]


