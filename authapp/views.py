from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
import django.contrib.auth as auth1

from django.contrib.auth import logout, authenticate, login, get_user_model
from authapp.models import CustomUser
from django.contrib.auth import logout,login as auth_login
from django.contrib.auth.views import LoginView
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from .decorators import school_auth
from authapp.forms import CustomUserCreationForm,School_info,Teacher_info
from django.shortcuts import render, HttpResponseRedirect

from school.models import *
def logout(request):
    # Log out the user.
    auth1.logout(request)
    # Return to homepage.
    return redirect('login')


def home( request):
    return render(request,'home.html')



def register_school( request):
    if request.method =='POST':
            form =CustomUserCreationForm(request.POST)
            info_form =School_info(request.POST)
            if form.is_valid() and info_form.is_valid():
                print("form is va;id")
                user=form.save(commit =False)
                user.email =user.email.lower()
                user.active =False
                user.is_school=True
                user.save()
                school_info=info_form.save(commit=False)
                school_info.s_info=user
                school_info.save()
                return redirect('login')
    form=CustomUserCreationForm()
    info_form=School_info()
    return render(request,'register_school.html',{'form':form,'info_form':info_form})


def register_teacher( request):
    if request.method =='POST':
            form =CustomUserCreationForm(request.POST)
            info_form =Teacher_info(request.POST)
            if form.is_valid() and info_form.is_valid():
                print("form is va;id")
                user=form.save(commit =False)
                user.email =user.email.lower()
                user.username=user.email
                user.active =False
                user.is_teacher=True
                user.save()
                teacher_info=info_form.save(commit=False)
                teacher_info.t_info=user
                school=School.objects.get(s_info__username=request.user)
                teacher_info.t_school=school
                teacher_info.save()
                return redirect('school_home')
    form=CustomUserCreationForm()
    info_form=Teacher_info()
    return render(request,'register_teacher.html',{'form':form,'info_form':info_form})

def login(request):
    if request.method == 'POST':
   
        # AuthenticationForm_can_also_be_used__
   
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            print(user,"--------------------------,")
            form = auth_login(request, user)
            
            messages.success(request, f' wecome {username} !!')
            if user.is_school:
                 return redirect('school_home')
            elif user.is_govt:
                return redirect('govt_home')
            elif user.is_teacher:
                return redirect('teacher_home')



        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()

    return render(request,'login.html', {'form':form,})

def school_home(request):


        return render(request,'school_home.html')

def govt_home(request):
    return render(request,'govt_home.html')

def teacher_home(request):
    students=Student.objects.filter(student_teacher__t_info__email=request.user)
    context={
        'students':students
    }
    return render(request,'teacher_home.html',context)
