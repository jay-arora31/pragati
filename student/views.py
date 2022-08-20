from django.shortcuts import render

# Create your views here.


from hashlib import new
from urllib import request
from django.shortcuts import render
from distutils.command import check
import imp
from multiprocessing import context
from django.shortcuts import redirect, render
import pandas as pd
import operator
from authapp.forms import CustomUserCreationForm

import teacher
from .models import *
from school.forms import *
from django.contrib import messages
from authapp.models import *
from teacher.models import *


def student_result(request):
    print(request.user)
    student_data=StudentAccount.objects.get(s_info__email=request.user)
    print("ROll",student_data.student_info.student_roll)
    print("CLass",student_data.student_info.student_class)
    print("Session",student_data.student_info.student_session)
    print("email",student_data.s_school.s_info.email)
    print()
    student_report_data=TestMark.objects.filter(
        student_info__student_roll=student_data.student_info.student_roll,
        student_info__student_class=student_data.student_info.student_class,
        student_info__student_session=student_data.student_info.student_session,
        school__s_info__email=student_data.s_school.s_info.email


    )
    student_marks_dict={}
    subjects_list=[]
    for i in student_report_data:
        subjects_list.append(i.subject.subject_name)
    newlist=set(subjects_list)
    newlist1=list(newlist)
    print(newlist1,"list")
    for i in newlist1:
        student_report_data1=TestMark.objects.filter(
        student_info__student_roll=student_data.student_info.student_roll,
        student_info__student_class=student_data.student_info.student_class,
        student_info__student_session=student_data.student_info.student_session,
        school__s_info__email=student_data.s_school.s_info.email,
        subject__subject_name=i

        )
        new_dict={}
        for j in student_report_data1:
            if j.test_type.test_name in new_dict:
                new_dict[j.test_type.test_name]+=j.obtain_mark
            else:
                new_dict[j.test_type.test_name]=j.obtain_mark
        
        student_marks_dict[i]=new_dict

    subject_lisst=[]
    for i in newlist1:
        subject_lisst.append(i)
    student_co_dict={}
    for a in subject_lisst:
        print("Hey sunbject",a)
        new_dict1={}
        student_report_data12=TestMark.objects.filter(
        student_info__student_roll=student_data.student_info.student_roll,
        student_info__student_class=student_data.student_info.student_class,
        student_info__student_session=student_data.student_info.student_session,
        school__s_info__email=student_data.s_school.s_info.email,
        subject__subject_name=a

        )
        outcome_data=AssignOutcome.objects.filter(
                school__s_info__email=student_data.s_school.s_info.email,
                subject__subject_name=a,
                test__session=student_data.student_info.student_session,
                subject__subject_class= student_data.student_info.student_class)
        heading_list=[]
        heading_list.append('Roll')
        outcome_dict={}
        for i in outcome_data:
                print(i.question_no)
                print(i.course_ot)
                print(i.test.test_name)
                if i.course_ot in outcome_dict:
                    if i.course_ot not in heading_list:
                        heading_list.append(i.course_ot)
                    outcome_dict[i.course_ot]+=i.mark
                else:
                    outcome_dict[i.course_ot]=i.mark
        print(outcome_dict)
        grade_dict1={}
        student_co_dict[a]=grade_dict1
        for j in student_report_data12:
                    if j.question_info.course_ot in new_dict1:
                            new_dict1[j.question_info.course_ot]+=j.obtain_mark
                    else:
                            new_dict1[j.question_info.course_ot]=j.obtain_mark

                    print("if new dict",new_dict1)  
                 
        for key,value in new_dict1.items():
            if value>=outcome_dict[key]*0.6:
                grade_dict1[key]=(True)
            else:
                grade_dict1[key]=(False)

    print(student_co_dict)
    print(student_marks_dict)
    context={
        'student_marks_dict':student_marks_dict,
        'student_co_dict':student_co_dict
    }

    return render(request,'view_result.html',context)
