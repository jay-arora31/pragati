from hashlib import new
from lib2to3.pgen2.literals import test
from urllib import request
from django.shortcuts import render
from distutils.command import check
import imp
from multiprocessing import context
from django.shortcuts import redirect, render
import pandas as pd
import operator
from authapp.forms import CustomUserCreationForm,CustomUserCreationForm1

import teacher
from .models import *
from school.forms import *
from django.contrib import messages
from authapp.models import *
from teacher.models import *
from .forms import *
# Create your views here.
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def filter_class_subject(request):
    classes=SchoolAssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
    teacher_classes=[]

    for i in classes:
        session=[]
        print(i.course_name.subject_info.subject_class)
        session.append(i.course_session)
        teacher_classes.append(i.course_name.subject_info.subject_class)
        
    class_filter=set(teacher_classes)
    teacher_classes=[]
    teacher_classes=list(class_filter)
    print(session)


    context={
    'teacher_classes':teacher_classes,
    'classes':classes,
    'session':session
    }
    return render(request,'filter_class_subject.html',context)


###############===================================Add Student manually and from excel=================############################


def add_student(request):
    if request.method == 'GET':
            print("Hey I am in POST")
            class_no = request.GET.get('student_class')
            print(class_no)
            session = request.GET.get('course_session')

            print(session,"Session")
            session1=[]
            session1.append(session)
            print(session1)
          
            form =AddStudentForm(request.GET)
            form2 =CustomUserCreationForm1(request.GET)
            if form.is_valid() and form2.is_valid():
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
                    student_form.save()
                    student_foorm=form2.save(commit =False)
                    student_foorm.is_student=True
                    student_foorm.username=student_foorm.email
                    student_foorm.save()
                    student_cred=StudentAccount(student_info=student_form,s_school=school,s_info=student_foorm)
                    student_cred.save()
                    
             
                    form=AddStudentForm()
                    form2=CustomUserCreationForm1()
                    context={
                        'student_class':class_no,
                        'student_session':session1,
                        'form2':form2,
                        'form':form,
                    }
                    messages.success(request, 'Student added successfully')

                    return render(request,'add_student.html',context )
            fform=AddStudentForm()
            form2=CustomUserCreationForm1()
            context={
                        'student_class':class_no,
                        'student_session':session1,
                        'form':form,
                        'form2':form2
                    }
            return render(request,'add_student.html',context )

def add_student_excel(request):
    if request.method=='POST':
            course_class = request.POST['course_class']
            course_session = request.POST['course_session']
            #course_subject = request.POST['subject']
            actual_file = request.FILES['actual_file_name']
            print(course_class)
            print("Hey Uploading data")

            print(actual_file)
            df=pd.read_csv(actual_file,)
            df.reset_index(drop=True)
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            for i in range(len(df)):
                print("Data Saving from excel student")
                print("course_class",course_class)
                print("course_session",course_session)
                #print("course_subject",course_subject)
                print("Student Roll",df['StudentRoll'][i])
                print("Student Name",df['StudentName'][i])
          
                print(df)
                student_obj=Student(student_roll=df['StudentRoll'][i],student_name=df['StudentName'][i],student_teacher=teacher,student_school=school,student_class=course_class,student_session=course_session)
                student_obj.save()
            return redirect('add_student_excel')
    classes=SchoolAssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
    teacher_classes=[]
    teacher_session=[]
    course_subjects=[]
    for i in classes:
        print(i.course_name.subject_info.subject_class)
       
        course_subjects.append(i.course_name.subject_info.subject_name)
        teacher_classes.append(i.course_name.subject_info.subject_class)
    class_filter=set(teacher_classes)
    session_filter=set(teacher_session)
    teacher_classes=[]
    teacher_session=[]
    teacher_classes=list(class_filter)
    teacher_session=list(session_filter)
    teacher_classes.sort()
    teacher_session.sort()
    context={
    'course_classes':teacher_classes,
    'course_session':teacher_session,
    'classes':classes,
    'course_subjects':course_subjects
    }
    return render(request,'add_students_excel.html',context )

##################################################=========End of Student add=====================###################
def add_test(request):
    if request.method == 'POST':
            form=AddTestForm(request.POST)
            subject = request.POST['subject']
            testtype = request.POST['test_type']
            course_class = request.POST['course_class']
            session = request.POST['session']
            noque1 = request.POST['noque']
            tot = request.POST['tot']
            noque=int(noque1)
            mark_list=[]
            question_list=[]
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            bind_data=school_class_subject.objects.get(subject_info__subject_name=subject,subject_info__subject_class=course_class)
            obj=SchoolAddTest(test_name=testtype,total_marks=tot,no_que=noque,subject_info=bind_data,teacher=teacher,school=school,session=session)
            obj.save()
            '''
           
            tot=0
            count=0
            mark=0
            for i in range(noque):
                count+=1
                mark=request.POST.get('mark'+str(i),'')
                new_mark=int(mark)
                tot+=tot+new_mark
            obj=SchoolAddTest(test_name=testtype,total_marks=tot,no_que=noque,subject_info=bind_data,teacher=teacher,school=school)
            obj.save()
            for i in range(noque):
                count+=1
                mark=request.POST.get('mark'+str(i),'')

                que=request.POST.get('que'+str(i),'')
                print(mark)
                print(que)
                markobj=SchoolAssignOutcome(question_no=count,course_ot=count,ques_info=que,mark=mark,teacher=teacher,school=school,test=obj)

                markobj.save()
'''


    form=AddTestForm()
    subjects=SchoolAssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)

    context={
        'form':form,
        'subjects':subjects,
    }
    return render(request,'add_test.html',context )

def add_test_next(request):
    if request.method == 'POST':
            form=AddTestForm(request.POST)
            subject = request.POST['subject']
            testtype = request.POST['testtype']
            course_class = request.POST['course_class']
            session = request.POST['session']
            noque1 = request.POST['noque']
            tot = request.POST['tot']

            noque=int(noque1)
            for i in range(noque+1):
                i=i+1
                mark=request.POST.get('mark'+str(i),'')
                print(mark)
                co=request.POST.get('text'+str(i),'')
                print(co)
                que=request.POST.get('question'+str(i),'')
                print(que)
         
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            bind_data=school_class_subject.objects.get(subject_info__subject_name=subject,subject_info__subject_class=course_class,subject_school__s_info__email=teacher.t_school.s_info.email)
   
            tot=0
            count=0
            mark=0

            obj=SchoolAddTest(test_name=testtype,total_marks=tot,no_que=noque,subject_info=bind_data,teacher=teacher,school=school)
            obj.save()
            for i in range(noque):
                i=i+1
                mark=request.POST.get('mark'+str(i),'')
                print(mark)
               

                co=request.POST.get('text'+str(i),'')
                print(co)
                que=request.POST.get('question'+str(i),'')
                print(que)
                markobj=SchoolAssignOutcome(question_no=i,course_ot=co,ques_info=que,mark=mark,teacher=teacher,school=school,test=obj)

                markobj.save()

    if request.method == 'GET':

            subject = request.GET.get('subject')
            testtype = request.GET.get('test_type')
            course_class = request.GET.get('course_class')
            session = request.GET.get('session')
            noque1 = request.GET.get('noque')
            noque1=int(noque1)
            tot = request.GET.get('tot')
            for_list=[]
            for i in range(noque1):
                for_list.append(0)
            course_outcome=GovtAssignOutcome.objects.filter(ot_class__subject_name=subject,ot_class__subject_class=course_class)
            ot_list=[]
            count1=0
            for i in course_outcome:
                ot_list.append(i.ot_name)
                count1=count1+1
            context={
                'subject':subject,
                'testtype':testtype,
                'course_class':course_class,
                'session':session,
                'noque1':noque1,
                'tot':tot,
                'for_list':for_list,
                'ot_list':ot_list,
                  'count1':count1

            }
            return render(request,'add_test_next.html',context )


    form=AddTestForm()
    subjects=SchoolAssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)

    context={
        'form':form,
        'subjects':subjects,
      
    }
    return render(request,'add_test.html',context )


def view_all_test(request):
    teacher=Teacher.objects.get(t_info__email=request.user)
    school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
    tests=SchoolAddTest.objects.filter(school=school,teacher__t_info__email=request.user)
    context={
        'tests':tests,
    }
    print(tests)
    return render(request,'view_all_tests.html',context )


def select_test_outcome(request):
    tests=AddTest.objects.filter(teacher__t_info__email=request.user)
    class_list1=[]
    session_data=[]
    for i in tests:
        class_list1.append(i.test_class)
        session_data.append(i.session)
    list_temp=set(class_list1)
    session1=set(session_data)
    session_list=list(session1)
    class_list=list(list_temp)
    context={
        'tests':tests,
        'class_list':class_list,
        'session_list':session_list
    }
    return render(request,'select_test_outcome.html',context )

def class_subject_test(request):
          data = {}
          if request.GET.get('test_subject', None) is not None:
              course_class = request.GET.get('course_class')
              test_subject = request.GET.get('test_subject')
              teacher=Teacher.objects.get(t_info__email=request.user)
              subjects=AddTest.objects.filter(subject__subject_name=test_subject,subject__subject_class=course_class,teacher__t_info__email=request.user)
              print(subjects)
              subject_data=[]
              for i in subjects:
                print(i.test_name)
                subject_data.append(i.test_name)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['subject_data']=subject_data
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)


def teacher_select_wise_subject(request):
          data = {}
          if request.GET.get('course_class', None) is not None:
              course_class = request.GET.get('course_class')
              teacher=Teacher.objects.get(t_info__email=request.user)
              subjects=school_class_subject.objects.filter(subject_info__subject_class=course_class,subject_school__s_info__email=teacher.t_school.s_info.email)
              print(subjects)
              subject_data=[]
              for i in subjects:
                print(i.subject_info.subject_name)
                subject_data.append(i.subject_info.subject_name)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['subject_data']=subject_data
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)

'''
def class_subject_wise_tests(request):
          data = {}
          if request.GET.get('course_class', None) is not None:
              course_class = request.GET.get('course_class')
              teacher=Teacher.objects.get(t_info__email=request.user)
              subjects=class_subject.objects.filter(subject_class=course_class,subject_school__s_info__email=teacher.t_school.s_info.email)
              print(subjects)
              subject_data=[]
              for i in subjects:
                print(i.subject_name)
                subject_data.append(i.subject_name)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['subject_data']=subject_data
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)

'''

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
                data_marks=request.POST.get('mark'+str(i),'')
                print(data_marks)
                print(choice)
                teacher=Teacher.objects.get(t_info__email=request.user)
                school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
                subject_data=class_subject.objects.get(subject_school__s_info__email=teacher.t_school.s_info.email,subject_name=test_subject,subject_class=test_class)
                test_data=AddTest.objects.get(test_name=test_type,teacher__t_info__email=request.user,subject__subject_name=test_subject,test_class=test_class,session=test_session,school__s_info__email=teacher.t_school.s_info.email)
                obj=AssignOutcome(test=test_data,question_no=i,course_ot=choice,mark=data_marks,subject=subject_data,school=school,teacher=teacher)
                obj.save()
            return redirect('teacher_home')

def select_subject_test(request):
    tests=SchoolAssignOutcome.objects.filter(teacher__t_info=request.user)
    print("Hey")
    session1=[]
    class_all=[]
    subjects=[]

    for i in tests:
        subjects.append(i.test.subject_info.subject_info.subject_name)
        class_all.append(i.test.subject_info.subject_info.subject_class)

   

    class_all1=set(class_all)
    class_all2=[]
    class_all2=list(class_all1)

    subjects1=set(subjects)
    subject_all=[]
    subject_all=list(subjects1)
    context={
        'tests':tests,

        'class_all':class_all2,
        'subjects':subject_all,
    }
    return render(request,'select_subject_test.html',context )



def add_student_marks(request):
        if request.method=='GET':
            test_class1 = request.GET.get('test_class')
            test_session1 = request.GET.get('test_session')
            test_subject1 = request.GET.get('test_subject')
            test_type1 = request.GET.get('test_type')
            print(test_type1)
            test_class=[]
            test_session=[]
            test_subject=[]
            test_type=[]
            test_class.append(test_class1)
            test_session.append(test_session1)
            test_subject.append(test_subject1)
            test_type.append(test_type1)
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)


            test_data=SchoolAddTest.objects.filter(test_name=test_type1,teacher__t_info__email=request.user,
            subject_info__subject_info__subject_name=test_subject1,
            subject_info__subject_info__subject_class=test_class1,
            school__s_info__email=teacher.t_school.s_info.email)
            print(test_data)
            student_data=Student.objects.filter(student_class=test_class1,student_session=test_session1,student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)
            print("wkjbwiS",student_data)
            for i in test_data:
                
                question_count=i.no_que
                total_mark=i.total_marks
            print(question_count,total_mark)
            question_marks=SchoolAssignOutcome.objects.filter(teacher__t_info__email=request.user,test__test_name=test_type1,
            test__subject_info__subject_info__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
            mark_box_count=0
            questions=[]
            for i in question_marks:
                mark_box_count=mark_box_count+1
                questions.append(i.ques_info)
            print(mark_box_count)
            course_outcome=GovtAssignOutcome.objects.filter(ot_class__subject_name=test_subject1,ot_class__subject_class=test_class1)
            ot_list=[]
            count1=0
            for i in course_outcome:
                ot_list.append(i.ot_name)
            context={
                'test_class':test_class,
                'test_session':test_session,
                'test_subject':test_subject,
                'test_type':test_type,
                'test_data':test_data,
                'question_marks':question_marks,
                'mark_box_count':mark_box_count,
                'student_data':student_data,
                'questions':questions,
                'ot_list':ot_list

            }
            return render(request,'add_student_marks.html',context )
        if request.method=='POST':
            test_class1 = request.POST['test_class']
            test_session1 = request.POST['test_session']
            test_subject1 = request.POST['test_subject']
            test_type1 = request.POST['test_type']
            student_roll1 = request.POST['student_roll']
            print(test_type1)
            test_class=[]
            test_session=[]
            test_subject=[]
            test_type=[]
            test_class.append(test_class1)
            test_session.append(test_session1)
            test_subject.append(test_subject1)
            test_type.append(test_type1)
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)


            test_data=SchoolAddTest.objects.filter(test_name=test_type1,teacher__t_info__email=request.user,
            subject_info__subject_info__subject_name=test_subject1,
            subject_info__subject_info__subject_class=test_class1,
            school__s_info__email=teacher.t_school.s_info.email)  
            print("Test data",test_data)       

            print()   
            for i in test_data:
                question_count=i.no_que
                total_mark=i.total_marks
            print(question_count,total_mark)
            question_marks1=SchoolAssignOutcome.objects.filter(teacher__t_info__email=request.user,test__test_name=test_type1,test__subject_info__subject_info__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
            mark_box_count=0
            for i in question_marks1:
                mark_box_count=mark_box_count+1
                print(i.question_no)
            data_checking=request.POST.get('mark1')
            student_data=Student.objects.filter(student_class=test_class1,student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)




            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            subject_data=school_class_subject.objects.get(subject_school__s_info__email=teacher.t_school.s_info.email,subject_info__subject_name=test_subject1,subject_info__subject_class=test_class1)
            print(subject_data)
            test_data=SchoolAddTest.objects.get(test_name=test_type1,teacher__t_info__email=request.user,subject_info__subject_info__subject_name=test_subject1,subject_info__subject_info__subject_class=test_class1,school__s_info__email=teacher.t_school.s_info.email)
            student=Student.objects.get(student_roll=student_roll1,student_class=test_class1,student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)
            checking=TestMark.objects.filter(subject__subject_info__subject_name=test_subject1,student_info__student_roll=student_roll1,test_type__test_name=test_type1,teacher__t_info__email=request.user,school__s_info__email=teacher.t_school.s_info.email)
            print(checking.exists())
            print(checking)
            print(checking.count() == 0,"checking.count() == 0")




            if checking.count() == 0:
                print('Hey')
                for i in range(mark_box_count):
                    i=i+1
                    print(i,"Hey I am I")
                    
                    que_info=SchoolAssignOutcome.objects.get(question_no=i,teacher__t_info__email=request.user,test__test_name=test_type1,test__subject_info__subject_info__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
                    data_marks=request.POST.get('mark'+str(i),'')
                    print(data_marks)
                    obj=TestMark(subject_class=test_class1,subject_data=test_subject1,teacher=teacher,student_info=student,question_info=que_info,obtain_mark=data_marks,test_type=test_data,subject=subject_data,school=school)
                    print("Save")
                    obj.save()
            global context1
            context1={
                'test_class':test_class,
                'test_session':test_session,
                'test_subject':test_subject,
                'test_type':test_type,
                'test_data':test_data,
                'question_marks':question_marks1,
                'mark_box_count':mark_box_count,
                'student_data':student_data

            }
        return render(request,'add_student_marks.html',context1 )

def add_marks_excel(request):
    if request.method=='POST':
            test_class1 = request.POST['test_class']
            test_session1 = request.POST['test_session']
            test_subject1 = request.POST['test_subject']
            test_type1 = request.POST['test_type']
            actual_file = request.FILES['actual_file_name']
            print(actual_file)
            print("Hey Uploading data")
            
            print(actual_file)
            df=pd.read_csv(actual_file,)
            df.reset_index(drop=True)
            print(df.head(5))
            print(test_type1)
            test_class=[]
            test_session=[]
            test_subject=[]
            test_type=[]
            test_class.append(test_class1)
            test_session.append(test_session1)
            test_subject.append(test_subject1)
            test_type.append(test_type1)
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            test_data=AddTest.objects.filter(test_name=test_type1,teacher__t_info__email=request.user,subject__subject_name=test_subject1,test_class=test_class1,session=test_session1,school__s_info__email=teacher.t_school.s_info.email)
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            subject_data=class_subject.objects.get(subject_school__s_info__email=teacher.t_school.s_info.email,subject_name=test_subject1,subject_class=test_class1)
            test_data=AddTest.objects.get(test_name=test_type1,teacher__t_info__email=request.user,subject__subject_name=test_subject1,test_class=test_class1,session=test_session1,school__s_info__email=teacher.t_school.s_info.email)
            question_marks1=AssignOutcome.objects.filter(teacher__t_info__email=request.user,test__test_name=test_type1,test__session=test_session1,subject__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
            mark_box_count=0
            for i in question_marks1:
                        mark_box_count=mark_box_count+1
                        print(i.question_no)
            count=0
            for i in range(len(df)):
                for j in range(mark_box_count):
                    count+=1
                    data_marks=df.iloc[i][j+1]
                    que_info=AssignOutcome.objects.get(question_no=j+1,teacher__t_info__email=request.user,test__test_name=test_type1,test__session=test_session1,subject__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
                    #data_marks=request.POST.get('mark'+str(i),'')
                    student=Student.objects.get(student_roll=df.iloc[i][0],student_class=test_class1,student_session=test_session1,student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)
                    obj=TestMark(teacher=teacher,
                    student_info=student,
                    question_info=que_info,
                    obtain_mark=data_marks,test_type=test_data,subject=subject_data,school=school)
                    print("Save")
                    obj.save()
                
            return render(request,'add_marks_excel.html' )

    tests=AssignOutcome.objects.filter(teacher__t_info=request.user)
    print("Hey")
    session1=[]
    class_all=[]
    subjects=[]
    for i in tests:
        session1.append(i.test.session)
        class_all.append(i.test.test_class)
        subjects.append(i.subject.subject_name)

    session2=set(session1)
    session=list(session2)

    class_all1=set(class_all)
    class_all2=[]
    class_all2=list(class_all1)

    subjects1=set(subjects)
    subject_all=[]
    subject_all=list(subjects1)
    context={
        'tests':tests,
        'session':session,
        'class_all':class_all2,
        'subjects':subject_all,
    } 

    return render(request,'add_marks_excel.html',context )


from django.http import JsonResponse


def filter_class_subject1(request):
          data = {}
          if request.GET.get('student_class', None) is not None:
              student_class = request.GET.get('student_class')

              teacher=Teacher.objects.get(t_info__email=request.user)

              subjects=class_subject.objects.filter(subject_class=student_class,subject_school__s_info__email=teacher.t_school.s_info.email)
              print(subjects)
              subject_data=[]
              for i in subjects:
                subject_data.append(i.subject_name)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['subject_data']=subject_data
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)




def add_student_filter_class_subject(request):
          data = {}
          print("Hey I am In function")
          if request.GET.get('course_class', None) is not None:
              
              course_class = request.GET.get('course_class')

              teacher=Teacher.objects.get(t_info__email=request.user)

              sessions=AssignedTeacher.objects.filter(course_class=course_class,course_teacher__t_info__email=request.user,course_school__s_info__email=teacher.t_school.s_info.email)
              print("hey I am in subject session")
              session_list=[]
              for i in sessions:
                if i.course_session not in session_list:
                    session_list.append(i.course_session)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['session_list']=session_list
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)



def view_student(request):
    teacher=Teacher.objects.get(t_info__email=request.user)

    students=Student.objects.filter(student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)
    context={
        'students':students
    }
    return render(request,'view_students.html',context )


def filter_student_marks_outcomes1(request):
        teacher=Teacher.objects.get(t_info__email=request.user)

        data=AssignOutcome.objects.filter(
            teacher__t_info__email=request.user,
            school__s_info__email=teacher.t_school.s_info.email,
        )
        image_bool=False
        if request.method=='POST':
            image_bool=True

            session=request.POST['session']
            subject=request.POST['subject']
            subject_class=request.POST['subject_class']
            print(subject,"Subject")
            data=SchoolAssignOutcome.objects.filter(
            teacher__t_info__email=request.user,
            school__s_info__email=teacher.t_school.s_info.email,
        )
            teacher=Teacher.objects.get(t_info__email=request.user)
            outcome_data=SchoolAssignOutcome.objects.filter(
                teacher__t_info__email=request.user,
                school__s_info__email=teacher.t_school.s_info.email,
                test__subject_info__subject_info__subject_name=subject,
               
                test__subject_info__subject_info__subject_class= subject_class)
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
                    outcome_dict[i.course_ot]+=int(i.mark)
                else:
                    outcome_dict[i.course_ot]=int(i.mark)
            teacher=Teacher.objects.get(t_info__email=request.user)
            student=TestMark.objects.filter(
                teacher__t_info__email=request.user,
                school__s_info__email=teacher.t_school.s_info.email,
                subject__subject_info__subject_name=subject,

                subject__subject_info__subject_class=subject_class
            )
            student_dict={
            }
            for i in student:
                new_dict={}
                if i.student_info.student_roll not in student_dict:
                    student_dict[i.student_info.student_roll]=new_dict
                    for j in student:
                        if j.student_info.student_roll==i.student_info.student_roll:
                            if j.question_info.course_ot in new_dict:
                                new_dict[j.question_info.course_ot]+=int(j.obtain_mark)
                            else:
                                new_dict[j.question_info.course_ot]=int(j.obtain_mark)
            student_dict_keys=list(student_dict.keys())
            print("Outcome dict",outcome_dict)
            print("Student Dict",student_dict)
            print(student_dict_keys)
            iteration=0
            all_over_dict={}
            for i in student_dict:
                    print(i)
                    roll=student_dict_keys[iteration]
                    iteration+=1
                    grade_dict={}
                    all_over_dict[roll]=grade_dict
                    student_list=[]
                    student_list.append(roll)
                    for j in student_dict[i]:
                        check_value=int(student_dict[i][j])
                        out_check=int(outcome_dict[j])
                        if check_value>=out_check*0.8:
                            grade_dict[j]=(True)
                        else:
                            grade_dict[j]=(False)
            print(all_over_dict)
            dic2={}
            for i in sorted(outcome_dict):
                dic2[i]=outcome_dict[i]
            co_head=list(dic2.keys())
            print(dic2)
            context={
                'all_over_dict':all_over_dict,
                'heading_list':heading_list,
                'data':data,
                'image_bool':image_bool,
                'co_head':co_head
            }

            return render(request,'view_student_outcome_view.html' ,context)
        context={
            'data':data,
            'image_bool':image_bool
        }
        return render(request,'view_student_outcome_view.html' ,context)








#######################################====================Sports Section========================################################




def select_sport(request):
    if request.method=='POST':
            sport_name=request.POST['sport_name']
            sport_level=request.POST['sport_level']
            sport_rank=request.POST['sport_rank']
            sport_classes=request.POST['sport_classes']
            sport_session=request.POST['sport_session']
            roll=request.POST['roll']
            print(
                "Data Printing",
            sport_name,
            sport_level,
            sport_rank,
            sport_classes,
            sport_session,
            roll
                
            )
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            studentinfo=Student.objects.get(
                student_roll=roll,
                student_class=sport_classes,
                student_session=sport_session,
                student_school__s_info__email=teacher.t_school.s_info.email,


              )
            sport_obj=Sports(
                student_info=studentinfo,
                sport_name=sport_name,
                sport_level=sport_level,
                sport_rank=sport_rank,
                sport_class=sport_classes,
                sport_session=sport_session,
                school=school,
                teacher=teacher
            )
            sport_obj.save()
            return redirect('select_sport')
    classes=AssignSportTeacher.objects.filter(sport_teacher__t_info__email=request.user)
    sport_classes=[]
    for i in classes:
        sport_classes.append(i.sport_class)
    context={
        'sport_classes':sport_classes,
    }
    return render(request,'sport/select_sport.html' ,context)


def select_cultural(request):
    if request.method=='POST':
            sport_name=request.POST['sport_name']
            sport_level=request.POST['sport_level']
            sport_rank=request.POST['sport_rank']
            sport_classes=request.POST['sport_classes']
            sport_session=request.POST['sport_session']
            roll=request.POST['roll']
            print(
                "Data Printing",
            sport_name,
            sport_level,
            sport_rank,
            sport_classes,
            sport_session,
            roll
                
            )
            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            studentinfo=Student.objects.get(
                student_roll=roll,
                student_class=sport_classes,
                student_session=sport_session,
                student_school__s_info__email=teacher.t_school.s_info.email,


              )
            sport_obj=Cultural(
                student_info=studentinfo,
                cultural_name=sport_name,
                cultural_level=sport_level,
                cultural_rank=sport_rank,
                cultural_class=sport_classes,
                cultural_session=sport_session,
                school=school,
                teacher=teacher
            )
            sport_obj.save()
            return redirect('select_cultural')
    classes=AssignCulturalTeacher.objects.filter(cul_teacher__t_info__email=request.user)
    sport_classes=[]
    for i in classes:
        sport_classes.append(i.sport_class)
    context={
        'sport_classes':sport_classes,
    }
    return render(request,'cultural/add_achieve.html' ,context)


def view_sport(request):
    data=Sports.objects.filter(teacher__t_info__email=request.user)
    context={
        'data':data
    }
    return render(request,'sport/view_sports.html',context)

def sport_filter_session(request):
          data = {}
          print("Hey I am In function")
          if request.GET.get('sport_class', None) is not None:
              
              course_class = request.GET.get('sport_class')

              teacher=Teacher.objects.get(t_info__email=request.user)

              sessions=AssignSportTeacher.objects.filter(sport_class=course_class,sport_teacher__t_info__email=request.user,sport_school__s_info__email=teacher.t_school.s_info.email)
              print("hey I am in subject session")

              session_list=[]
              for i in sessions:
                if i.sport_session not in session_list:
                    session_list.append(i.sport_session)
              print("Session list",session_list)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['session_list']=session_list
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)




def sport_filter_session(request):
          data = {}
          print("Hey I am In function")
          if request.GET.get('sport_class', None) is not None:
              
              course_class = request.GET.get('sport_class')

              teacher=Teacher.objects.get(t_info__email=request.user)

              sessions=AssignSportTeacher.objects.filter(sport_teacher__t_info__email=request.user,sport_school__s_info__email=teacher.t_school.s_info.email)
              print("hey I am in subject session")

              session_list=[]
              for i in sessions:
                if i.sport_session not in session_list:
                    session_list.append(i.sport_session)
              print("Session list",session_list)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['session_list']=session_list
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)





def sport_filter_roll(request):
          data = {}
          print("Hey I am In function")
          if request.GET.get('sport_class', None) is not None:
              
              course_class = request.GET.get('sport_class')
              sport_session = request.GET.get('sport_session')
              print(course_class,sport_session)
              teacher=Teacher.objects.get(t_info__email=request.user)
              students=Student.objects.filter(
                student_class=course_class,
                student_session=sport_session,
                student_school__s_info__email=teacher.t_school.s_info.email,


              )
              print("hey I am in subject session")
              print(students)
              roll_list=[]
              for i in students:
                    roll_list.append(i.student_roll)
              print("roll_list list",roll_list)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['roll_list']=roll_list
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)


# Creates a sorted dictionary (sorted by key)
from collections import OrderedDict
import numpy as np 

def testing_function(request):
            teacher=Teacher.objects.get(t_info__email=request.user)
            outcome_data=AssignOutcome.objects.filter(
                teacher__t_info__email=request.user,
                school__s_info__email=teacher.t_school.s_info.email,
                subject__subject_name='English',
                test__session='2022-2023',
                subject__subject_class= '1')
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
            student=TestMark.objects.filter(
                student_info__student_roll=101,
                teacher__t_info__email=request.user,
                school__s_info__email=teacher.t_school.s_info.email,
                subject__subject_name='English',
                test_type__session='2022-2023',
                subject__subject_class='1'
            )
            print(student)
            student_dict={
            }
            new_dict={}
            
            for j in student:
                        if j.question_info.course_ot in new_dict:
                            new_dict[j.question_info.course_ot]+=j.obtain_mark
                        else:
                            new_dict[j.question_info.course_ot]=j.obtain_mark
            student_dict_keys=list(student_dict.keys())
            print("Outcome dict",outcome_dict)
            print("Student Dict",new_dict)

            for key,value in outcome_dict.items():
                if key not in new_dict:
                        new_dict[key]=0

            sorted_dict= dict(sorted(new_dict.items(), key=lambda item: item[1])) 
            sorted_dict_outcome= dict(sorted(outcome_dict.items(), key=lambda item: item[1])) 

            print("Sorted new dict",sorted_dict)

            print("Sorted Outcome dict",sorted_dict_outcome)
            grade_list=[]
            for i in sorted_dict:
                        if sorted_dict[i]>=sorted_dict_outcome[i]*0.6:
                            grade_list.append(True)
                        else:
                            grade_list.append(False)
            print(grade_list,"Grade list")
            return render(request,'testing_template.html' )








def testing_function_login(request):
    class_count=0
    subject_count=0
    school=School.objects.all()
    student_all_over_dict={}
    for i in school:
        print(i.s_info.email)
        school_email=i.s_info.email
        class_list=[]

        classes=class_subject.objects.filter(subject_school__s_info__email=school_email)
        for a in classes:
            if a.subject_class not in class_list:
                class_list.append(a.subject_class)
        for class_single in class_list:
            print("==================================class single=====================")
            class_count+=1
            subject_list=[]
            class_data=class_single
            student_dict={}
            subjects=class_subject.objects.filter(subject_school__s_info__email=school_email,subject_class=class_data)
            subject_count_data=class_subject.objects.filter(subject_school__s_info__email=school_email,subject_class=class_data).count()
            student_check_dict={}
            for i in subjects:
                subject_count+=1
                subject_data=i.subject_name
                outcome_data=AssignOutcome.objects.filter(
                school__s_info__email=school_email,
                subject__subject_name=subject_data,
                test__session='2022-2023',
                subject__subject_class= class_data)
                heading_list=[]
                heading_list.append('Roll')
                outcome_dict={}
                for i in outcome_data:
                    if i.course_ot in outcome_dict:
                            if i.course_ot not in heading_list:
                                heading_list.append(i.course_ot)
                            outcome_dict[i.course_ot]+=i.mark
                    else:
                        outcome_dict[i.course_ot]=i.mark
                student=TestMark.objects.filter(
                school__s_info__email=school_email,
                subject__subject_name=subject_data,
                test_type__session='2022-2023',
                subject__subject_class=class_data
                )
                print(student)
                student_dict={}

                for i in student:
                    new_dict={}
                    if i.student_info.student_roll not in student_dict:
                        student_dict[i.student_info.student_roll]=new_dict
                        for j in student:
                            if j.student_info.student_roll==i.student_info.student_roll:
                                if j.question_info.course_ot in new_dict:
                                    new_dict[j.question_info.course_ot]+=j.obtain_mark
                                else:
                                    new_dict[j.question_info.course_ot]=j.obtain_mark
                student_dict_keys=list(student_dict.keys())
                iteration=0
                all_over_dict={}
                for i in student_dict:

                        roll=i
                        iteration+=1
                        grade_dict={}
                        all_over_dict[roll]=grade_dict
                        student_list=[]
                        student_list.append(roll)
                        for j in student_dict[i]:
                            if student_dict[i][j]>=outcome_dict[j]*0.6:
                                grade_dict[j]=True  
                            else:
                                grade_dict[j]=False
                        print(grade_dict)
                        grade_list=list(grade_dict.values())
                        final_check = all(grade_list)
                        if final_check:
                            if roll in student_check_dict:
                                student_check_dict[roll]+=1
                            else:
                                student_check_dict[roll]=1


                print("Student check list",student_check_dict)
                for key,value in student_check_dict.items():
                    print("Value of dict",value)
                    if value==subject_count_data:
                        key=str(school_email)
                        if key in student_all_over_dict:
                            student_all_over_dict[school_email]+=1
                        else:
                            student_all_over_dict[school_email]=1
        print("Student_Check DIct value",student_all_over_dict)

        sorted_d = dict( sorted(student_all_over_dict.items(), key=operator.itemgetter(1),reverse=True))
        print('Dictionary in descending order by value : ',sorted_d)
        school_list=[]
        for i in sorted_d:
            school_names=School.objects.get(s_info__email=i)
            school_list.append(school_names.s_name)
        print(school_list)
    context={
        'sorted_d':sorted_d,
        'school_list':school_list
    }
    return render(request,'testing_template.html',context )





def add_subject_outcome(request):
    print("jayyyyy")
    teacher_data=AssignedTeacher.objects.filter(course_teacher__t_info=request.user)
    session_data=[]
    for i in teacher_data: 
        session_data.append(i.course_session)
        
    context={
        'session_data':session_data
    }
    return render(request,'testing_template.html',context )
