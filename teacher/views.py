from urllib import request
from django.shortcuts import render
from distutils.command import check
import imp
from multiprocessing import context
from django.shortcuts import redirect, render

import teacher
from .models import *
from school.forms import *
from django.contrib import messages
from authapp.models import *
from teacher.models import *
from .forms import *
# Create your views here.



def filter_class_subject(request):
    classes=AssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
    teacher_classes=[]
    teacher_session=[]
    for i in classes:
        print(i.course_class)
        print(i.course_session)
        teacher_classes.append(i.course_class)
        teacher_session.append(i.course_session)
    class_filter=set(teacher_classes)
    session_filter=set(teacher_session)
    teacher_classes=[]
    teacher_session=[]
    teacher_classes=list(class_filter)
    teacher_session=list(session_filter)
    context={
    'teacher_classes':teacher_classes,
    'teacher_session':teacher_session,
    'classes':classes
    }
    return render(request,'filter_class_subject.html',context)





def add_student(request):
    if request.method == 'GET':
            print("Hey I am in POST")
            class_no = request.GET.get('student_class')
            print(class_no)
            session = request.GET.get('student_session')

            print(session,"Session")
            session1=[]
            session1.append(session)
            print(session1)
            subject =request.GET.get('subject')
            print(subject)
            subject1=[]
            subject1.append(subject)
            print(subject1)
            form =AddStudentForm(request.GET)
            if form.is_valid():
                print("Hey Form is va;id")
                student_form=form.save(commit =False)
                print(student_form.student_name is None)
                
                if student_form.student_name is not None:

                    teacher=Teacher.objects.get(t_info__email=request.user)
                    school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
                    student_form.student_school=school
                    student_form.student_teacher=teacher
                    student_form.student_class=class_no
                    student_form.student_session=session
                    student_form.student_course_name=subject
                    student_form.save()
                            
                    form=AddStudentForm()
                    context={
                        'student_class':class_no,
                        'student_session':session1,
                        'subject':subject1,
                        'form':form,
                    }
                    return render(request,'add_student.html',context )
            form=AddStudentForm()
            context={
                        'student_class':class_no,
                        'student_session':session1,
                        'subject':subject1,
                        'form':form,
                    }
            return render(request,'add_student.html',context )


def add_test(request):
    if request.method == 'POST':
            form=AddTestForm(request.POST)
            subject = request.POST['subject']
            session = request.POST['session']

            if form.is_valid():
                add_test_form=form.save(commit =False)

                teacher=Teacher.objects.get(t_info__email=request.user)
                school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
                add_test_form.school= school
                add_test_form.teacher=teacher
                test_class=add_test_form.test_class
                add_test_form.subject=class_subject.objects.get(subject_name=subject,subject_class=test_class,subject_school=school)
                add_test_form.session=session
                add_test_form.save()

                form=AddTestForm()
                subjects=AssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
                for i in subjects:
                    print(i.course_name.subject_name)
                context={
                    'form':form,
                    'subjects':subjects,
                }
                return render(request,'add_test.html',context )



    form=AddTestForm()
    subjects=AssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
    for i in subjects:
        print(i.course_name.subject_name)
    context={
        'form':form,
        'subjects':subjects,
    }
    return render(request,'add_test.html',context )



def view_all_test(request):
    teacher=Teacher.objects.get(t_info__email=request.user)
    school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
    tests=AddTest.objects.filter(school=school)
    context={
        'tests':tests,
    }
    return render(request,'view_all_tests.html',context )


def select_test_outcome(request):
    tests=AddTest.objects.filter(teacher__t_info__email=request.user)
    context={
        'tests':tests,
    }
    return render(request,'select_test_outcome.html',context )



def add_question_outcome(request):
    if request.method == 'GET':
            test_class = request.GET.get('test_class')
            test_session = request.GET.get('test_session')
            test_subject = request.GET.get('test_subject')
            test_type = request.GET.get('test_type')
            
            print(test_type)
            test_type1=[]
            test_subject1=[]
            test_session1=[]
            test_subject1.append(test_subject)
            test_type1.append(test_type)
            test_session1.append(test_session)
            no_question=AddTest.objects.filter(teacher__t_info__email=request.user,test_class=test_class,session=test_session,subject__subject_name=test_subject,test_name=test_type)
            print(no_question)
            count=0
            co_count=0
            for i in no_question:
                    count=i.no_que
                    co_count=i.subject.subject_learning
  
            print(count)
            check=[]
            for i in range(count):  
                i=i+1
                choice = request.POST.get('text'+str(i),'')
                print(choice)
                print('text'+str(i),'')
                print('outcome',choice)
            print("List==================================",check)
            context={
                'test_class':test_class,
                'test_session':test_session1,
                'test_subject':test_subject1,
                'test_type':test_type1,
                'count':count,
                'co_count':co_count
            }
            return render(request,'add_test_outcome.html',context )
    if request.method=='POST':
            test_class = request.POST['test_class']
            test_session = request.POST['test_session']
            test_subject = request.POST['test_subject']
            test_type = request.POST['test_type']
            no_question=AddTest.objects.filter(teacher__t_info__email=request.user,test_class=test_class,session=test_session,subject__subject_name=test_subject,test_name=test_type)
            print(no_question)
            count=0
            co_count=0
            for i in no_question:
                    count=i.no_que
                    co_count=i.subject.subject_learning
  
            print(count)
            check=[]
            for i in range(count):  
                i=i+1
                choice = request.POST.get('text'+str(i),'')
                print(choice)
                teacher=Teacher.objects.get(t_info__email=request.user)
                school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
                subject_data=class_subject.objects.get(subject_school__s_info__email=teacher.t_school.s_info.email,subject_name=test_subject,subject_class=test_class)
                test_data=AddTest.objects.get(test_name=test_type,teacher__t_info__email=request.user,subject__subject_name=test_subject,test_class=test_class,session=test_session,school__s_info__email=teacher.t_school.s_info.email)
                obj=AssignOutcome(test=test_data,question_no=i,course_ot=choice,subject=subject_data,school=school,teacher=teacher)
                obj.save()
            return redirect('teacher_home')

