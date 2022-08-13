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



class TestMark(models.Model):
    student_info=models.ForeignKey( Student, on_delete=models.CASCADE)
    question_info=models.ForeignKey( AssignOutcome, on_delete=models.CASCADE)
    obtain_mark=models.IntegerField(null=True,blank=True)
    test_type=models.ForeignKey( AddTest, on_delete=models.CASCADE)
    subject =models.ForeignKey( class_subject, on_delete=models.CASCADE)
    school =models.ForeignKey( School, on_delete=models.CASCADE)
    teacher =models.ForeignKey( Teacher, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.question_info.question_no)

