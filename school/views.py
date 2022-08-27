from cgi import print_directory
from distutils.command import check
import imp
from multiprocessing import context
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from authapp.models import *
from teacher.models import *
from authapp.forms import *


from django.shortcuts import get_object_or_404,render,HttpResponseRedirect
 
def assign_teacher(request):
    if request.method == 'POST':
                email = request.POST['t_email']
                name = request.POST['t_name']
                session = request.POST['session']
                course_class = request.POST['course_class']
                course_subject = request.POST['course_subject']


                teacher=Teacher.objects.get(t_info__email=email)
                school=School.objects.get(s_info__email=request.user)

                

                checking=SchoolAssignedTeacher.objects.filter(course_name__subject_info__subject_name=course_subject,course_name__subject_info__subject_class=course_class,course_school__s_info__email=request.user)
                if not checking.exists():
                    bind_datac=school_class_subject.objects.get(subject_info__subject_name=course_subject,subject_info__subject_class=course_class,subject_school__s_info__email=request.user)

                    obj=SchoolAssignedTeacher(course_name=bind_datac,course_teacher=teacher,course_school=school,course_session=session)
                    obj.save()
                    messages.success(request,"Teacher Successfully Assigned to Class")
                else:
                    messages.error(request,"Teacher Already Assigned to Class")
                    
    subject_data=GovtSubject.objects.all()
    class_data=[]
    for i in subject_data:
        class_data.append(i.subject_class)
        print("i.subject_class",i.subject_class)
    subject_class1=set(class_data)
    print(subject_class1)
    subject_data2=list(subject_class1)
    print(subject_data2)
    form=AssignCourseTeacher()
    teachers=Teacher.objects.filter(t_school__s_info__email=request.user)
    sessions=SchoolSessions.objects.all()
    for i in teachers:
        print(i.t_name)
        print(i.t_info.email)
    return render(request,'assign_teacher.html', {'form':form,'teachers':teachers,'sessions':sessions,'subject_data':subject_data2})

def class_wise_subject(request):
          data = {}
          if request.GET.get('course_class', None) is not None:
              course_class = request.GET.get('course_class')

              subjects=class_subject.objects.filter(subject_class=course_class,subject_school__s_info__email=request.user)
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
def teacher_namewise_email(request):
          data = {}
          if request.GET.get('teacher_name', None) is not None:
              teacher_name = request.GET.get('teacher_name')
              print(teacher_name)

              email_data=Teacher.objects.filter(t_name=teacher_name,t_school__s_info__email=request.user)
              print(email_data)
              email_data1=[]
              for i in email_data:
                email_data1.append(i.t_info.email)
              data['result'] = True
              data['message'] = "Note posted successfully"
              data['email_data']=email_data1
              ...
          if request.is_ajax():
             return JsonResponse(data)
          else:
             return JsonResponse(data)
   
def teacher_view(request):
    teachers=Teacher.objects.filter(t_school__s_info__email=request.user)
    for i in teachers:
        print("------------Teachers_name")
        print(i.t_name)
    context={
        'teachers':teachers,
    }
    return render(request,'teacher_view.html',context)

def teacher_delete(request,id):
    teacher_id=id
    obj = get_object_or_404(CustomUser, id = teacher_id)
    obj.delete()
    messages.error(request,"Teacher Deleted")
    return redirect('teacher_view')

def select_student(request):
    classes=AssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
    teacher_classes=[]
    teacher_session=[]
    for i in classes:
        print(i.course_class)
        print(i.course_session)
        teacher_classes.append(i.course_class)
        teacher_session.append(i.course_session)
    form=AddStudentForm()
    class_filter=set(teacher_classes)
    session_filter=set(teacher_session)
    teacher_classes=[]
    teacher_session=[]
    teacher_classes=list(class_filter)
    teacher_session=list(session_filter)
    context={
    'teacher_classes':teacher_classes,
    'teacher_session':teacher_session}
    return render(request,'teacher/select_student.html',context)


def add_marks(request):
    if request.method == 'GET':
 
        student_class=request.GET.get('student_class')
        
        student_roll=request.GET.get('student_roll')
        student_session=request.GET.get('student_session')
        print(student_session)
        if student_roll is not None:
            student_info1=Student.objects.get(student_roll=student_roll,student_class=student_class,student_session=student_session,student_teacher__t_info__username=request.user)

        form =AddMarks(request.GET)
        if form.is_valid() and student_roll is not None:
            student_marks=form.save(commit =False)
            print("-----------------English",student_marks.eng)
            student_marks.student_info=student_info1
            student_marks.save()
            print("")
        result=Student.objects.filter(student_teacher__t_info__email=request.user,student_class=student_class,student_session=student_session)
        for i in range(1):
            print(i)

        form=AddMarks()
        context={
            'student_class':student_class,
            'student_session':student_session,
            'form':form,
            'result':result
        }
        
        return render(request,'teacher/add_marks.html',context)


def submit_marks(request):
    if request.method == 'POST':

         form =AddMarks(request.POST)
         if form.is_valid():
            student_marks=form.save(commit =False)
            print(student_marks.eng)
 
            return redirect('add_marks')



def assign_subject(request):
    if request.method=='POST':
            course_class=request.POST['course_class']
            course_subject=request.POST['course_subject']
            checking=school_class_subject.objects.filter(subject_info__subject_name=course_subject,subject_school__s_info__email=request.user)
            if not checking.exists():
                bind_data=GovtSubject.objects.get(subject_name=course_subject,subject_class=course_class)
                school=School.objects.get(s_info__email=request.user)
                obj=school_class_subject(subject_info=bind_data,subject_school=school)
                obj.save()
                messages.success(request,"Subject added to class successfully")
            else:
                messages.error(request,"Already Added Subject to this class")

    subject_data=GovtSubject.objects.all()
    class_data=[]
    for i in subject_data:
        class_data.append(i.subject_class)
        print("i.subject_class",i.subject_class)
    subject_class1=set(class_data)
    print(subject_class1)
    subject_data2=list(subject_class1)
    print(subject_data2)
    context={
        'subject_class':subject_data2,
      
    }
    return render(request,'school/assign_subject.html',context)





def govt_class_wise_subject(request):
          data = {}
          if request.GET.get('course_class', None) is not None:
              course_class = request.GET.get('course_class')

              subjects=GovtSubject.objects.filter(subject_class=course_class)
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


from django.db.models import Count

def view_subjects(request):
    filter_subject=class_subject.objects.filter(subject_school__s_info__email=request.user)
    print(filter_subject)
    dic={}
    value=0
    for i in filter_subject:
        if i.subject_class in dic:
            dic[i.subject_class]+=value
        else:      
            value=1 
            dic[i.subject_class]=value

    sort_data =sorted(dic.items(), key=lambda x: x[1])
    sort_data_dict = dict(sort_data)

    print(dic)
    context1={
        'dic':sort_data_dict
    }
    return render(request,'school/view_class_subjects.html',context1)


def view_class_subjects(request,key):
    class_subject1=key
    filter_subject=class_subject.objects.filter(subject_school__s_info__email=request.user,subject_class=class_subject1)
    context={
        'data':filter_subject,
        'class_no':class_subject1
    }
    return render(request,'school/view_specific_class.html',context)


    
def subject_delete(request,id):
    obj = get_object_or_404(class_subject, id = id)
    obj.delete()
    return redirect('school_home')



from django.http import JsonResponse

def get_topics_ajax(request):
    if request.method == "POST":
        print("Hey I am in ajax function")
        subject_class=request.POST.get('data')
        print(subject_class)
        try:
            subject = class_subject.objects.filter(subject_class = subject_class,subject_school__s_info__email=request.user)
        except Exception:
            print("Error in Ajax")
        return JsonResponse(list(subject.values('subject_name')), safe = False) 


def view_assigned_teachers(request):
        subjects=SchoolAssignedTeacher.objects.filter(course_school__s_info__email=request.user)
        for i in subjects:
            print(i.course_name.subject_info.subject_name)

        context={
            'subjects': subjects
        }    
        return render(request,'school/view_assigned_teachers.html',context)
    




########################################============================Sport Section =======================#################################



def assign_sport_teacher(request):
    if request.method=='POST':
        sport_class=request.POST['sport_class']
        #t_name=request.POST['t_name']
        t_email=request.POST['t_email']
        session=request.POST['session']
        teacher=Teacher.objects.get(t_info__email=t_email)
        school=School.objects.get(s_info__email=request.user)
        sport_obj=AssignSportTeacher(
            sport_class=sport_class,
            sport_teacher=teacher,
            sport_school=school,
            sport_session=session
            
            )
        sport_obj.save()
        return redirect('assign_sport_teacher')
    teachers=Teacher.objects.filter(t_school__s_info__email=request.user)
    sessions=SchoolSessions.objects.all()
    for i in teachers:
        print(i.t_name)
        print(i.t_info.email)
    context={
        'sessions':sessions,
        'teachers':teachers
    }
    return render(request,'school_sport/assign_sport_teacher.html',context)





def assign_cultural_teacher(request):
    if request.method=='POST':
        sport_class=request.POST['sport_class']
        #t_name=request.POST['t_name']
        t_email=request.POST['t_email']
        session=request.POST['session']
        teacher=Teacher.objects.get(t_info__email=t_email)
        school=School.objects.get(s_info__email=request.user)
        sport_obj=AssignCulturalTeacher(
            cul_class=sport_class,
            cul_teacher=teacher,
            cul_school=school,
            cul_session=session
            
            )
        sport_obj.save()
        return redirect('assign_cultural_teacher')
    teachers=Teacher.objects.filter(t_school__s_info__email=request.user)
    sessions=SchoolSessions.objects.all()
    for i in teachers:
        print(i.t_name)
        print(i.t_info.email)
    context={
        'sessions':sessions,
        'teachers':teachers
    }
    return render(request,'cultural/assign_sport_teacher.html',context)


def student_register(request):
    form=CustomUserCreationForm()
    context={
        'form':form
    }
    return render(request,'student_template/student_register.html',context)



def view_sports_teacher(request):
    sport_data=AssignSportTeacher.objects.filter(sport_school__s_info__email=request.user)
    context={
        'sport_data':sport_data
    }
    return render(request,'school_sport/view_assigned_sport.html',context)
