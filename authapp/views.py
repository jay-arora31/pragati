from email import message
from multiprocessing import context
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
import django.contrib.auth as auth1
import operator
from django.contrib.auth import logout, authenticate, login, get_user_model
from authapp.models import CustomUser, GovtAssignOutcome
from django.contrib.auth import logout,login as auth_login
from django.contrib.auth.views import LoginView
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from .decorators import school_auth
from authapp.forms import CustomUserCreationForm,School_info,Teacher_info,CustomUserCreationForm1,add_subject_gov
from django.shortcuts import render, HttpResponseRedirect
import plotly.express as px
from .models import *

from school.models import *

from teacher.models import *
def logout(request):
    # Log out the user.
    auth1.logout(request)
    # Return to homepage.
    return redirect('login')


def home( request):
    return render(request,'home.html')



def register_school( request):
    if request.method =='POST':
            district=request.POST['district']
            city=request.POST['city']


            form =CustomUserCreationForm(request.POST)
            info_form =School_info(request.POST)
            if form.is_valid() and info_form.is_valid():
                print("form is va;id")
                user=form.save(commit =False)
                user.email =user.email.lower()
                user.username=user.email
                user.is_active =False
                user.is_school=True
                user.save()
                school_info=info_form.save(commit=False)
                school_info.s_district=district
                school_info.s_city=city
                school_info.s_info=user

                school_info.s_info=user
                school_info.save()
                return redirect('login')
    form=CustomUserCreationForm()
    info_form=School_info()
    return render(request,'register_school.html',{'form':form,'info_form':info_form})


def register_teacher( request):
    if request.method =='POST':
            form =CustomUserCreationForm1(request.POST)
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
                messages.success(request,"Teacher Added Successfully")
                return redirect('register_teacher')
    form=CustomUserCreationForm1()
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
            elif user.is_student:
                return redirect('student_home')




        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    school_form=CustomUserCreationForm()
    school_info_form=School_info()
    return render(request,'login.html', {'form':form,'school_form':school_form,'school_info_form':school_info_form})

def school_home(request):
    student=Student.objects.filter(student_school__s_info__email=request.user)
    data=[]
    for i in student:
        print(i.student_class)
        data.append("Class "+str(i.student_class))
        print(i.student_class)

    fig = px.histogram(
        x=data,
        
        title="Student Count",
        labels={'x': 'Classes'}
    )
    fig.update_layout(yaxis_title="Number of Students")

    chart = fig.to_html()
    sport_data=Sports.objects.filter(school__s_info__email=request.user)
    points=0
    for i in sport_data:
        print(i.sport_name)
        print(i.sport_name=='National')
        if i.sport_level=='National':
            if i.sport_rank=='1st Rank':
                points+=12
            elif i.sport_rank=='2nd Rank':
                points+=8
            elif i.sport_rank=='3rd Rank':
                points+=4
        elif i.sport_level=='State':
            if i.sport_rank=='1st Rank':
                points+=9
            elif i.sport_rank=='2nd Rank':
                points+=6
            elif i.sport_rank=='3rd Rank':
                points+=3
        elif i.sport_level=='School':
            if i.sport_rank=='1st Rank':
                points+=6
            elif i.sport_rank=='2nd Rank':
                points+=4
            elif i.sport_rank=='3rd Rank':
                points+=2
        elif i.sport_level=='participated':
                points+=1
    print("Pointsss",points)
    cal=points%5
    print("Division",cal)
    points=points-cal
    points=points/5
    print("Badges Count",int(points))
    points=int(points)
    return render(request,'school_home.html',context={'chart': chart,'sport_badges':points})

def govt_home(request):
    class_count=0
    subject_count=0
    school=School.objects.all()
    student_all_over_dict={}
    
    for i in school:
        print("=====================Hey School=========================")
        print(i.s_info.email)
        print(i.s_name)
        school_email=i.s_info.email
        class_list=[]

        classes=school_class_subject.objects.filter(subject_school__s_info__email=school_email)
        for a in classes:
            if a.subject_info.subject_class not in class_list:
                class_list.append(a.subject_info.subject_class)
        for class_single in class_list:
            print("==================================class single=====================")
            class_count+=1
            subject_list=[]
            class_data=class_single
            student_dict={}
            subjects=school_class_subject.objects.filter(subject_school__s_info__email=school_email,subject_info__subject_class=class_data)
            subject_count_data=school_class_subject.objects.filter(subject_school__s_info__email=school_email,subject_info__subject_class=class_data).count()
            student_check_dict={}
            for i in subjects:



                subject_count+=1
                subject_data=i.subject_info.subject_name
                outcome_data=SchoolAssignOutcome.objects.filter(
                school__s_info__email=school_email,
                test__subject_info__subject_info__subject_name=subject_data,
                 test__subject_info__subject_info__subject_class= class_data)
                heading_list=[]
                heading_list.append('Roll')
                outcome_dict={}
                for i in outcome_data:
                    if i.course_ot in outcome_dict:
                            if i.course_ot not in heading_list:
                                heading_list.append(i.course_ot)
                            outcome_dict[i.course_ot]+=int(i.mark)
                    else:
                        outcome_dict[i.course_ot]=int(i.mark)
                student=TestMark.objects.filter(
                school__s_info__email=school_email,
                subject__subject_info__subject_name=subject_data,
             
                subject__subject_info__subject_class=class_data
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
                                    new_dict[j.question_info.course_ot]+=int(j.obtain_mark)
                                else:
                                    new_dict[j.question_info.course_ot]=int(j.obtain_mark)
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
        school_email_list=sorted_d.keys()
        sports_point=[]

        for email in school_email_list:
            sport_data=Sports.objects.filter(school__s_info__email=email)
            print("School email")
            print(sports_point)

            points=0
            for i in sport_data:
                print("Cal sports data")
                if i.sport_level=='National':
                    if i.sport_rank=='1st Rank':
                        points+=12
                    elif i.sport_rank=='2nd Rank':
                        points+=8
                    elif i.sport_rank=='3rd Rank':
                        points+=4
                elif i.sport_level=='State':
                    if i.sport_rank=='1st Rank':
                        points+=9
                    elif i.sport_rank=='2nd Rank':
                        points+=6
                    elif i.sport_rank=='3rd Rank':
                        points+=3
                elif i.sport_level=='School':
                    if i.sport_rank=='1st Rank':
                        points+=6
                    elif i.sport_rank=='2nd Rank':
                        points+=4
                    elif i.sport_rank=='3rd Rank':
                        points+=2
                elif i.sport_level=='participated':
                        points+=1
            
            sports_point.append(points)
            print("================Value ",points,"===================")
    print(sports_point)
    new_list=[1,2]
    again_dict={}
    for i in range(len(school_list)):
        print(school_list[i])
        sport_dict={}
        sport_dict['school']=school_list[i]
        sport_dict['points']=sports_point[i]
        sport_dict['cal']=new_list[i]
        again_dict[i]=sport_dict
    print(again_dict)

    context={
        'sorted_d':sorted_d,
        'school_list':school_list,
        'sports_point':sports_point,
        'again_dict':again_dict
    }
    return render(request,'govt_home.html',context)
import json


def school_view(request):
    school_data=School.objects.all()
    context={
        'school_data':school_data,
    }
    return render(request,'govtemplate/school_view.html',context)

def school_active(request,email):
    school_email=email
    obj_school=CustomUser.objects.get(email=school_email)
    print("Active function")
    print(obj_school)
    obj_school.is_active=True
    obj_school.save()
    return redirect('school_view')


def school_inactive(request,email):
    school_email=email
    obj_school=CustomUser.objects.get(email=school_email)
    print("Active function")
    print(obj_school)
    obj_school.is_active=False
    obj_school.save()
    return redirect('school_view')


def school_delete(request,email):
    school_email=email
    obj = get_object_or_404(School,s_info__email=school_email)
    print(obj)
    obj.delete()

    print("Delete function")
    return redirect('school_view')


def teacher_home(request):
    students=Student.objects.filter(student_teacher__t_info__email=request.user)
    data=[]
    for i in students:
        print(i.student_class)
        data.append("Class "+str(i.student_class))
        print(i.student_class)
 
    fig = px.histogram(
        x=data,
        
        title="Student Count",
        labels={'x': 'Classes'}
    )

    fig.update_layout(yaxis_title="Number of Students"
    ,
        xaxis = dict(           # attribures for x axis 
        showline = True,
        showgrid = True,
        linecolor = 'black',
        tickfont = dict(
            family = 'Calibri'
        )
    ),
    yaxis = dict(           # attribures for y axis 
        showline = True,
        showgrid = True,
        linecolor = 'black',
        tickfont = dict(
            family = 'Times New Roman'
        )
    ),
    plot_bgcolor = 'white' )
    class_data=data
    label1=set(data)
    labels=list(label1)
    class_data_list=[]
    class_data_list.append(class_data)
    chart = fig.to_html()
    data1=[1,1,1,1,2,3,3,3]
    course_list = ['Computer Science','Computer Science', 'Computer Engineering']
    print(class_data_list)
    context={
        'students':students,
        'chart':chart,
        'class_data':class_data,
        'labels':labels,
        'course_list':course_list,
        'data1':data1,
        'class_data_list':class_data_list
    }
    return render(request,'teacher_home.html',context)


def student_home(request):
    return render(request,'student_home.html')














#================================================Gov Views==============================

def gov_add_subject(request):
    if request.method=='POST':

        form=add_subject_gov(request.POST)
        no_ot=request.POST['noot']
      
        val=int(no_ot)
        print(type(val))
        if form.is_valid():
            subject_form=form.save(commit=False)

            subject_form.subject_learning=val
            subject_form.save()
            ot=0
            for i in range(val):
                ot+=1
                ot_name = request.POST.get('text'+str(i),'')

                obj_ot=GovtAssignOutcome(ot_no=ot,ot_name=ot_name,ot_class=subject_form)
                obj_ot.save()

    form=add_subject_gov()
    context={
        'form':form
    }


    return render(request,'govtemplate/add_subject.html',context)


def gov_view_subject(request):
    class_data=GovtSubject.objects.all().order_by('subject_class')
    print(class_data)
    context={
        'class_data':class_data
    }    
    return render(request,'govtemplate/view_subjects.html',context)


def gov_view_subject_delete(request,id):
    sub_id=id
    obj=GovtSubject.objects.get(id=id)
    obj.delete()
    messages.success(request,"Subject Deleted SuccessFully")   
    return redirect('gov_view_subject')

