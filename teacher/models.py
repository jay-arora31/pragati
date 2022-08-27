from django.db import models
from school.models import *

# Create your models here.
TEST_CHOICES= [
        ('Unit_Test_1', 'Unit Test 1'),
        ('Unit_Test_2', 'Unit Test 2'),
        ('Unit_Test_3', 'Unit Test 3'),
        ('Unit_Test_4', 'Unit Test 4'),
        ('Semester1', 'Semester 1'),
        ('Semester2', 'Semester 2'),

        ]

Sport_Choice= [
        ('School', 'School'),
        ('National', 'National'),
        ('State', 'State'),
       

        ]
Sport_Rank= [
        ('1st Rank', '1st Rank'),
        ('2nd Rank', '2nd Rank'),
        ('3rd Rank', '3rd Rank'),
        ]




class AddTest(models.Model):
    test_name=models.CharField(max_length =255, null=True,blank=True,choices=TEST_CHOICES)
    test_class=models.CharField(max_length =255, null=True,blank=True,choices=CLASS_CHOICES)
    total_marks=models.IntegerField( null=True,blank=True)
    no_que=models.IntegerField( null=True,blank=True)
    session=models.CharField(max_length =255, null=True,blank=True)
    subject =models.ForeignKey( class_subject, on_delete=models.CASCADE)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return self.test_name

class SchoolAddTest(models.Model):
    test_name=models.CharField(max_length =255, null=True,blank=True,choices=TEST_CHOICES)
    total_marks=models.CharField(max_length =255, null=True,blank=True)
    no_que=models.CharField(max_length =255, null=True,blank=True)
    session=models.CharField(max_length =255, null=True,blank=True)
    subject_info=models.ForeignKey( school_class_subject, on_delete=models.CASCADE)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return self.test_name

class SchoolAssignOutcome(models.Model):
    question_no=models.IntegerField( null=True,blank=True)
    course_ot=models.CharField(max_length =255, null=True,blank=True)
    mark=models.CharField(max_length =255, null=True,blank=True)
    ques_info=models.CharField(max_length =255, null=True,blank=True)
    test=models.ForeignKey( SchoolAddTest, on_delete=models.CASCADE)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)




class TestMark(models.Model):
    student_info=models.ForeignKey( Student, on_delete=models.CASCADE)
    subject_data=models.CharField(max_length =255, null=True,blank=True)
    subject_class=models.CharField(max_length =255, null=True,blank=True)
    question_info=models.ForeignKey( SchoolAssignOutcome, on_delete=models.CASCADE)
    obtain_mark=models.IntegerField(null=True,blank=True)
    test_type=models.ForeignKey( SchoolAddTest, on_delete=models.CASCADE)
    subject =models.ForeignKey( school_class_subject, on_delete=models.CASCADE)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.question_info.question_no)


class AssignOutcome(models.Model):
    question_no=models.IntegerField( null=True,blank=True)
    course_ot=models.CharField(max_length =255, null=True,blank=True)
    mark=models.IntegerField( null=True,blank=True)
    test=models.ForeignKey( AddTest, on_delete=models.CASCADE)
    subject =models.ForeignKey( class_subject, on_delete=models.CASCADE)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return self.school.s_name+"____"+self.subject.subject_name+"_____"+self.test.test_name+"___Class--"+self.subject.subject_class





class Sports(models.Model):
    student_info=models.ForeignKey( Student, on_delete=models.CASCADE)
    sport_name=models.CharField(max_length =255, null=True,blank=True)
    sport_level=models.CharField(max_length =255, null=True,blank=True)
    sport_rank=models.CharField(max_length =255, null=True,blank=True)
    sport_class=models.IntegerField(null=True,blank=True)
    sport_session=models.CharField(max_length =255, null=True,blank=True)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.student_info.student_name)


class Cultural(models.Model):
    student_info=models.ForeignKey( Student, on_delete=models.CASCADE)
    cultural_name=models.CharField(max_length =255, null=True,blank=True)
    cultural_rank=models.CharField(max_length =255, null=True,blank=True)
    cultural_level=models.CharField(max_length =255, null=True,blank=True)

    cultural_class=models.IntegerField(null=True,blank=True)
    cultural_session=models.CharField(max_length =255, null=True,blank=True)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.student_info.student_name)

class AcademicCount(models.Model):
    student_info=models.ForeignKey( Student, on_delete=models.CASCADE)
    academic_count=models.IntegerField(null=True,blank=True)
    school=models.ForeignKey( School, on_delete=models.CASCADE)
    subject=models.CharField(max_length =255, null=True,blank=True)
    academic_class=models.CharField(max_length =255, null=True,blank=True)

    def __str__(self):
        return str(self.school.s_name)