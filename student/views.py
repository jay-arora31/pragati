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

  

    student_report_data12=TestMark.objects.filter(
        student_info__student_roll=student_data.student_info.student_roll,
        student_info__student_class=student_data.student_info.student_class,
        school__s_info__email=student_data.s_school.s_info.email,
        subject_data='English'


    )
    print(student_report_data12)
    print()
    student_marks_dict={}
    subjects_list=[]
    for i in student_report_data12:
        subjects_list.append(i.subject_data)
    newlist=set(subjects_list)
    newlist1=list(newlist)
    print(newlist1,"list")
    for i in newlist1:
        student_report_data1=TestMark.objects.filter(
        student_info__student_roll=student_data.student_info.student_roll,
        student_info__student_class=student_data.student_info.student_class,
        school__s_info__email=student_data.s_school.s_info.email,
        subject__subject_info__subject_name=i

        )
        new_dict={}
        for j in student_report_data1:
            if j.test_type.test_name in new_dict:
                mark=int(j.obtain_mark)
                new_dict[j.test_type.test_name]+=mark
            else:
                mark1=j.obtain_mark
                new_dict[j.test_type.test_name]=mark1
        
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
        school__s_info__email=student_data.s_school.s_info.email,
        subject__subject_info__subject_name=a

        )




        outcome_data=SchoolAssignOutcome.objects.filter(
                school__s_info__email=student_data.s_school.s_info.email,
                test__subject_info__subject_info__subject_name=a,
                test__subject_info__subject_info__subject_class= student_data.student_info.student_class)
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
                        mark=int(i.mark)
                    outcome_dict[i.course_ot]+=mark
                else:
                    mark=int(i.mark)
                    outcome_dict[i.course_ot]=mark
        print("Hey",outcome_dict)
        grade_dict1={}
        student_co_dict[a]=grade_dict1
        for j in student_report_data12:
                    if j.question_info.course_ot in new_dict1:
                            new_dict1[j.question_info.course_ot]+=int(j.obtain_mark)
                    else:
                            new_dict1[j.question_info.course_ot]=int(j.obtain_mark)

                 
        for key,value in new_dict1.items():
            if value>=outcome_dict[key]*0.6:
                grade_dict1[key]=(True)
            else:
                grade_dict1[key]=(False)

 
    student_mark_dict={}
    sub_data=SchoolAssignOutcome.objects.filter(
                school__s_info__email=student_data.s_school.s_info.email,
                test__subject_info__subject_info__subject_name=a,
                test__subject_info__subject_info__subject_class= student_data.student_info.student_class)
    subjects1=[]
    multi_dict_student={}


    for i in sub_data:
        subjects1.append(i.test.subject_info.subject_info.subject_name)
    subject2=set(subjects1)
    real_subject=list(subject2)
    mark_dict={}

    for j in real_subject:
                student_mark_dict[j]=mark_dict

                single_sub=j
                sub_data22=SchoolAssignOutcome.objects.filter(
                school__s_info__email=student_data.s_school.s_info.email,
                test__subject_info__subject_info__subject_name=j,
                test__subject_info__subject_info__subject_class= student_data.student_info.student_class)
                test_list=[]

                subject_dict={}

                mark_dict['school_mark']=subject_dict
                for k in sub_data22:
                    test_list.append(k.test.test_name)
                test_list1=set(test_list)
                test_list_final=list(test_list1)


                for m in test_list_final:
                    sub_data23=SchoolAssignOutcome.objects.filter(
                    school__s_info__email=student_data.s_school.s_info.email,
                    test__subject_info__subject_info__subject_name=j,
                    test__subject_info__subject_info__subject_class= student_data.student_info.student_class,
                    test__test_name=m)
                    test_wise_dict={}
                    if m not in subject_dict:
                        subject_dict[m]=test_wise_dict
                    for o in sub_data23:

                            test_wise_dict[o.question_no]=i.mark

    for j in real_subject:
                student_data1=StudentAccount.objects.get(s_info__email=request.user)

 

                single_sub=j
                sub_data22=SchoolAssignOutcome.objects.filter(
                school__s_info__email=student_data.s_school.s_info.email,
                test__subject_info__subject_info__subject_name=j,
                test__subject_info__subject_info__subject_class= student_data.student_info.student_class)
                test_list=[]
                subject_dict={}

                mark_dict['student_mark']=subject_dict
                for k in sub_data22:
                    test_list.append(k.test.test_name)
                test_list1=set(test_list)
                test_list_final=list(test_list1)
                print(test_list_final)

                for m in test_list_final:
                    sub_data234=TestMark.objects.filter(
                    student_info__student_roll=student_data1.student_info.student_roll,
                    subject__subject_info__subject_name=j,
                    subject__subject_info__subject_class= student_data1.student_info.student_class,
                    test_type__test_name=m)
 
                    test_wise_dict1={}
                   
                    for o in sub_data234:
                            cat1=student_mark_dict[o.subject.subject_info.subject_name]['school_mark'][o.test_type.test_name][o.question_info.question_no]
                            new_val=str(str(o.obtain_mark)+"/"+str(cat1))
                            student_mark_dict[o.subject.subject_info.subject_name]['school_mark'][o.test_type.test_name][o.question_info.question_no]=new_val
                            test_wise_dict1[o.question_info.question_no]=o.obtain_mark
    test_lists=['Unit_Test_1','Unit_Test_2']
    print(student_marks_dict)
    context={
        'student_marks_dict':student_marks_dict,
        'student_mark_dict':student_mark_dict,
        'student_co_dict':student_co_dict,
        'test_lists':test_lists
    }
    print(student_mark_dict)
    return render(request,'view_result.html',context)
