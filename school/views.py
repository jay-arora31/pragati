from distutils.command import check
import imp
from multiprocessing import context
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from authapp.models import *


from django.shortcuts import get_object_or_404,render,HttpResponseRedirect
 
def assign_teacher(request):
    if request.method == 'POST':
            email = request.POST['t_email']
            name = request.POST['t_name']
            session = request.POST['session']
            form =AssignCourseTeacher(request.POST)
            print("------assign teacher")
            print(form.errors.as_data())
            if form.is_valid():
                print("------form valid teacher")
                assign_form=form.save(commit =False)
                teacher=Teacher.objects.get(t_info__email=email)
                school=School.objects.get(s_info__email=request.user)
                checking=AssignedTeacher.objects.filter(course_class=assign_form.course_class,course_session=session,course_school=school)
                
                print("checking email",email)
                print(checking)
                if not checking.exists():
                    assign_form.course_teacher=teacher
                    assign_form.course_school=school
                    assign_form.course_session=session
                    assign_form.save()
                    return redirect('school_home')
                else:
                    form=AssignCourseTeacher()
                    messages.error(request,"class already assigned")

                    teachers=Teacher.objects.filter(t_school__s_info__email=request.user)
                    sessions=SchoolSessions.objects.all()
                    for i in teachers:
                        print(i.t_name)
                        print(i.t_info.email)
                    return render(request,'assign_teacher.html', {'form':form,'teachers':teachers,'sessions':sessions})
    form=AssignCourseTeacher()
    teachers=Teacher.objects.filter(t_school__s_info__email=request.user)
    sessions=SchoolSessions.objects.all()
    for i in teachers:
        print(i.t_name)
        print(i.t_info.email)
    return render(request,'assign_teacher.html', {'form':form,'teachers':teachers,'sessions':sessions})


def add_student(request):
    if request.method == 'POST':
            class_no = request.POST['class']
            session = request.POST['session']
            form =AddStudentForm(request.POST)
            if form.is_valid():
                student_form=form.save(commit =False)
                teacher=Teacher.objects.get(t_info__email=request.user)
                school=School.objects.get(s_info__email=teacher.t_school.s_info.email)
                student_form.student_school=school
                student_form.student_teacher=teacher
                student_form.student_class=class_no
                student_form.student_session=session
                student_form.save()
                return redirect('teacher_home')

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
    context={'form':form,
    'teacher_classes':teacher_classes,
    'teacher_session':teacher_session}
    return render(request,'add_student.html',context )

                
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

