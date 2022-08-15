from hashlib import new
from urllib import request
from django.shortcuts import render
from distutils.command import check
import imp
from multiprocessing import context
from django.shortcuts import redirect, render
import pandas as pd

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
    teacher_classes.sort()
    teacher_session.sort()
    context={
    'teacher_classes':teacher_classes,
    'teacher_session':teacher_session,
    'classes':classes
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
                    student_form.save()
                            
                    form=AddStudentForm()
                    context={
                        'student_class':class_no,
                        'student_session':session1,
                      
                        'form':form,
                    }
                    return render(request,'add_student.html',context )
            form=AddStudentForm()
            context={
                        'student_class':class_no,
                        'student_session':session1,
                        'form':form,
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
    classes=AssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
    teacher_classes=[]
    teacher_session=[]
    course_subjects=[]
    for i in classes:
        print(i.course_class)
        print(i.course_session)
        course_subjects.append(i.course_name.subject_name)
        teacher_classes.append(i.course_class)
        teacher_session.append(i.course_session)
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
            test_data=AddTest.objects.filter(test_name=test_type1,teacher__t_info__email=request.user,subject__subject_name=test_subject1,test_class=test_class1,session=test_session1,school__s_info__email=teacher.t_school.s_info.email)
            student_data=Student.objects.filter(student_class=test_class1,student_session=test_session1,student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)
            print("wkjbwiS",student_data)
            for i in test_data:
                question_count=i.no_que
                total_mark=i.total_marks
            print(question_count,total_mark)
            question_marks=AssignOutcome.objects.filter(teacher__t_info__email=request.user,test__test_name=test_type1,test__session=test_session1,subject__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
            mark_box_count=0
            for i in question_marks:
                mark_box_count=mark_box_count+1
                
            context={
                'test_class':test_class,
                'test_session':test_session,
                'test_subject':test_subject,
                'test_type':test_type,
                'test_data':test_data,
                'question_marks':question_marks,
                'mark_box_count':mark_box_count,
                'student_data':student_data

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
            test_data=AddTest.objects.filter(test_name=test_type1,teacher__t_info__email=request.user,subject__subject_name=test_subject1,test_class=test_class1,session=test_session1,school__s_info__email=teacher.t_school.s_info.email)
            for i in test_data:
                question_count=i.no_que
                total_mark=i.total_marks
            print(question_count,total_mark)
            question_marks1=AssignOutcome.objects.filter(teacher__t_info__email=request.user,test__test_name=test_type1,test__session=test_session1,subject__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
            mark_box_count=0
            for i in question_marks1:
                mark_box_count=mark_box_count+1
                print(i.question_no)
            data_checking=request.POST.get('mark1')
            student_data=Student.objects.filter(student_class=test_class1,student_session=test_session1,student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)

            teacher=Teacher.objects.get(t_info__email=request.user)
            school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
            subject_data=class_subject.objects.get(subject_school__s_info__email=teacher.t_school.s_info.email,subject_name=test_subject1,subject_class=test_class1)
            test_data=AddTest.objects.get(test_name=test_type1,teacher__t_info__email=request.user,subject__subject_name=test_subject1,test_class=test_class1,session=test_session1,school__s_info__email=teacher.t_school.s_info.email)
            student=Student.objects.get(student_roll=student_roll1,student_class=test_class1,student_session=test_session1,student_teacher__t_info__email=request.user,student_school__s_info__email=teacher.t_school.s_info.email)
            checking=TestMark.objects.filter(student_info__student_roll=student_roll1,test_type__test_name=test_type1,test_type__session=test_session1,teacher__t_info__email=request.user,school__s_info__email=teacher.t_school.s_info.email)
            print(checking.exists())
            print(checking)
            print(checking.count() == 0,"checking.count() == 0")
            if checking.count() == 0:
                print('Hey')
                for i in range(mark_box_count):
                    i=i+1
                    print(i,"Hey I am I")
                    
                    que_info=AssignOutcome.objects.get(question_no=i,teacher__t_info__email=request.user,test__test_name=test_type1,test__session=test_session1,subject__subject_name=test_subject1,school__s_info__email=teacher.t_school.s_info.email)
                    data_marks=request.POST.get('mark'+str(i),'')
                    print(data_marks)
                    obj=TestMark(teacher=teacher,student_info=student,question_info=que_info,obtain_mark=data_marks,test_type=test_data,subject=subject_data,school=school)
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
        
        if request.method=='POST':
            session=request.POST['session']
            subject=request.POST['subject']
            subject_class=request.POST['subject_class']
            data=AssignOutcome.objects.filter(
            teacher__t_info__email=request.user,
            school__s_info__email=teacher.t_school.s_info.email,
        )
            teacher=Teacher.objects.get(t_info__email=request.user)
            outcome_data=AssignOutcome.objects.filter(
                teacher__t_info__email=request.user,
                school__s_info__email=teacher.t_school.s_info.email,
                subject__subject_name=subject,
                test__session=session,
                subject__subject_class= subject_class)
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
            teacher=Teacher.objects.get(t_info__email=request.user)
            student=TestMark.objects.filter(
                teacher__t_info__email=request.user,
                school__s_info__email=teacher.t_school.s_info.email,
                subject__subject_name=subject,
                test_type__session=session,
                subject__subject_class=subject_class
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
                                new_dict[j.question_info.course_ot]+=j.obtain_mark
                            else:
                                new_dict[j.question_info.course_ot]=j.obtain_mark
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
                        if student_dict[i][j]>=outcome_dict[j]*0.6:
                            grade_dict[j]=(True)
                        else:
                            grade_dict[j]=(False)
            print(all_over_dict)
            context={
                'all_over_dict':all_over_dict,
                'heading_list':heading_list,
                'data':data
            }

            return render(request,'view_student_outcome_view.html' ,context)
        context={
            'data':data
        }
        return render(request,'view_student_outcome_view.html' ,context)
