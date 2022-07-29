import imp
from django.shortcuts import redirect, render
from .models import *
from .forms import *

def assign_teacher(request):
    if request.method == 'POST':
            email = request.POST['t_email']
            name = request.POST['t_name']
            form =AssignCourseTeacher(request.POST)
            print("------assign teacher")
            print(form.errors.as_data())
            if form.is_valid():
                print("------form valid teacher")
                assign_form=form.save(commit =False)
                print("checking email",email)
                teacher=Teacher.objects.get(t_info__email=email)
                school=School.objects.get(s_info__email=request.user)
                assign_form.course_teacher=teacher
                assign_form.course_school=school
                assign_form.save()
                return redirect('school_home')
    form=AssignCourseTeacher()
    teachers=Teacher.objects.filter(t_school__s_info__email=request.user)
    for i in teachers:
        print(i.t_name)
        print(i.t_info.email)
    return render(request,'assign_teacher.html', {'form':form,'teachers':teachers})


def add_student(request):
    classes=AssignedTeacher.objects.filter(course_teacher__t_info__email=request.user)
    for i in classes:
        print(i.course_class)
    form=AddStudentForm()
    return render(request,'add_student.html', {'form':form})

                
