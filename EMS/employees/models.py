from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.



class employeeDetails(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  empcode=models.CharField(max_length=50)
  empdept=models.CharField(max_length=100, null=True)
  designation=models.CharField(max_length=100, null=True)
  contact=models.CharField(max_length=15, null=True)
  gender=models.CharField(max_length=50, null=True)
  join_date=models.DateField(null=True)
  def __str__(self):
    return self.user.username

class employeeEducation(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  # postgraduate
  coursepg=models.CharField(max_length=100,null=True)
  schoolclgpg=models.CharField(max_length=200, null=True)
  yearpasspg=models.CharField(max_length=20, null=True)
  percentpg=models.CharField(max_length=30, null=True)
  # graduate
  coursegra=models.CharField(max_length=100,null=True)
  schoolclggra=models.CharField(max_length=200, null=True)
  yearpassgra=models.CharField(max_length=20, null=True)
  percentgra=models.CharField(max_length=30, null=True)
  # senior secondary
  coursesc=models.CharField(max_length=100,null=True)
  schoolclgsc=models.CharField(max_length=200, null=True)
  yearpasssc=models.CharField(max_length=20, null=True)
  percentsc=models.CharField(max_length=30, null=True)
  def __str__(self):
    return self.user.username+" "+self.coursegra

class employeeExperience(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  # company 1
  comp1name=models.CharField(max_length=100,null=True)
  comp1desig=models.CharField(max_length=100, null=True)
  comp1sal=models.CharField(max_length=100, null=True)
  comp1dura=models.CharField(max_length=100, null=True)
  # company 2
  comp2name=models.CharField(max_length=100,null=True)
  comp2desig=models.CharField(max_length=100, null=True)
  comp2sal=models.CharField(max_length=100, null=True)
  comp2dura=models.CharField(max_length=100, null=True)
  # company 3
  comp3name=models.CharField(max_length=100,null=True)
  comp3desig=models.CharField(max_length=100, null=True)
  comp3sal=models.CharField(max_length=100, null=True)
  comp3dura=models.CharField(max_length=100, null=True)
  def __str__(self):
    return self.user.username+" "+self.comp1name