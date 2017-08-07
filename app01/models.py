from django.db import models

# Create your models here.

class Class(models.Model):
    cname=models.CharField(max_length=32)
class Student(models.Model):
    sname=models.CharField(max_length=32)
    clas=models.ForeignKey(Class)

class Teacher(models.Model):
    tname = models.CharField(max_length=32)
class Tea_Cla(models.Model):
    teacher=models.ForeignKey(Teacher)
    clas=models.ForeignKey(Class)
    class Meta:
        unique_together=(("teacher","clas"),)
class User_infor(models.Model):
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=64)
    class Meta:
        unique_together=(("name","pwd"),)

