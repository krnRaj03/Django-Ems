from email.errors import MessageError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail
from django.conf import settings

from requests import request
from .models import *
import datetime
from django.contrib import messages

#for pdfs
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


# def some_view(request):
#     # Create a file-like buffer to receive PDF data.
#     buffer = io.BytesIO()

#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(100, 100, "Hello world.")

#     # Close the PDF object cleanly, and we're done.
#     p.showPage()
#     p.save()

#     # FileResponse sets the Content-Disposition header so that browsers
#     # present the option to save the file.
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

# Create your views here.
def home(request):
  return render(request,'index.html')

#Admin Login
def adminLogin(request):
  if request.method=="POST":
    u=request.POST['username']
    p=request.POST['pass1']
    user=authenticate(username=u, password=p)
    if user.is_staff:
      login(request,user)
      error="NO"
    else:
      error="YES"
  return render(request,'admin/admin_login.html',locals())

#Employee Home
def admin_home(request):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  return render(request,'admin/admin_home.html')


#Employee Home
def emp_home(request):
  if not request.user.is_authenticated:
    return redirect("emp_login")
  
  now = datetime.datetime.now()
  x=now.strftime("%Y-%m-%d %H:%M:%S")
  return render(request,'emp/emp_home.html',{"datetime":x})


#Employee Logout
def Logout(request):
  logout(request)
  return redirect('home')

#Employee Experience
def myExp(request):
  if not request.user.is_authenticated:
    return redirect("emp_login")

  user=request.user
  experience=employeeExperience.objects.get(user=user)
  return render(request,'emp/my_exp.html',{'experience':experience})

#Employee Education
def myEdu(request):
  if not request.user.is_authenticated:
    return redirect("emp_login")

  user=request.user
  education=employeeEducation.objects.get(user=user)
  return render(request,'emp/my_edu.html',{'education':education})

 #Employee Login 
def emp_login(request):
  error=""
  if request.method=="POST":
    u=request.POST['usernameId']
    p=request.POST['pass1Id']
    user=authenticate(username=u, password=p)
    if user:
      login(request,user)
      
      error="NO"
    else:
      error="YES"
  return render(request,'emp/emp_login.html',locals())


#Employee Signup
def register(request):
  error=''
  if request.method=="POST":
    fn=request.POST['firstname']
    ln=request.POST['lastname']
    ec=request.POST['empcode']
    em=request.POST['email']
    pw=request.POST['pass1']

    try:
      user=User.objects.create_user(first_name=fn,last_name=ln,username=em, password=pw)
      employeeDetails.objects.create(user=user,empcode=ec)
      employeeEducation.objects.create(user=user)
      employeeExperience.objects.create(user=user)
      error="NO"
    except:
      error="YES"
  return render(request,'registration.html',locals())

#Employee Profile
def profile(request):
  if not request.user.is_authenticated:
    return redirect("emp_login")
  error=''
  user=request.user
  employee=employeeDetails.objects.get(user=user)
  if request.method=="POST":
    fn=request.POST['firstname']
    ln=request.POST['lastname']
    ec=request.POST['empcode']
    dept=request.POST['department']
    desig=request.POST['designation']
    cont=request.POST['contact']
    joindate=request.POST['jdate']
    gender=request.POST['gender']

    # updating user data
    employee.first_name=fn
    employee.last_name=ln
    employee.empcode=ec
    employee.empdept=dept
    employee.designation=desig
    employee.contact=cont
    employee.gender=gender

    if joindate:
      employee.join_date=joindate

    try:
      employee.save()
      employee.user.save()
      error="NO"
    except:
      error="YES"
  return render(request,'profile.html',locals())

#Employee editable Experience
def editExp(request,pid):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  error=""

  user=User.objects.get(id=pid)
  #instantiating the model as a variable 
  experience=employeeExperience.objects.get(user=user)

  if request.method=="POST":
    #Company1 Profile
    #P.S the name in [] & is same as Models & same as HTML name tags
    company1name=request.POST['comp1name']
    company1designation=request.POST['comp1desig']
    company1salary=request.POST['comp1sal']
    company1duration=request.POST['comp1dura']

    #Company2 Profile
    company2name=request.POST['comp2name']
    company2designation=request.POST['comp2desig']
    company2salary=request.POST['comp2sal']
    company2duration=request.POST['comp2dura']

    #Company3 Profile
    company3name=request.POST['comp3name']
    company3designation=request.POST['comp3desig']
    company3salary=request.POST['comp3sal']
    company3duration=request.POST['comp3dura']

    # updating user data
    #company1
    experience.comp1name=company1name
    experience.comp1desig=company1designation
    experience.comp1sal=company1salary
    experience.comp1dura=company1duration

    #company2
    experience.comp2name=company2name
    experience.comp2desig=company2designation
    experience.comp2sal=company2salary
    experience.comp2dura=company2duration

    #company3
    experience.comp3name=company3name
    experience.comp3desig=company3designation
    experience.comp3sal=company3salary
    experience.comp3dura=company3duration
    try:
      experience.save()
      experience.user.save()
      error="NO"
    except:
      error="YES"
  return render(request,'admin/edit_exp.html',locals())

  #Employee editable Experience
def editEdu(request,pid):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  error=""
  user=User.objects.get(id=pid)

  #instantiating the model as a variable 
  education=employeeEducation.objects.get(user=user)

  if request.method=="POST":
    #Company1 Profile
    #P.S the name in [] & is same as Models & same as HTML name tags
    pgCourse=request.POST['coursepg']
    pgCollege=request.POST['schoolclgpg']
    pgYear=request.POST['yearpasspg']
    pgPercent=request.POST['percentpg']

    #Company2 Profile
    gradCourse=request.POST['coursegra']
    gradCollege=request.POST['schoolclggra']
    gradYear=request.POST['yearpassgra']
    gradPercent=request.POST['percentgra']

    #Company3 Profile
    ssCourse=request.POST['coursesc']
    ssName=request.POST['schoolclgsc']
    ssYear=request.POST['yearpasssc']
    ssPercent=request.POST['percentsc']

    # updating user data
    #company1
    education.coursepg=pgCourse
    education.schoolclgpg=pgCollege
    education.yearpasspg=pgYear
    education.percentpg=pgPercent

    #company2
    education.coursegra=gradCourse
    education.schoolclggra=gradCollege
    education.yearpassgra=gradYear
    education.percentgra=gradPercent

    #company3
    education.coursesc=ssCourse
    education.schoolclgsc=ssName
    education.yearpasssc=ssYear
    education.percentsc=ssPercent
    try:
      education.save()
      education.user.save()
      error="NO"
    except:
      error="YES"
  return render(request,'admin/edit_edu.html',locals())

def changePass(request):
  if not request.user.is_authenticated:
    return redirect("emp_login")
  error=""
  user=request.user

  if request.method=="POST":
    current=request.POST['currentPass']
    new=request.POST['newPass']

    try:
      if user.check_password(current):
        user.set_password(new)
        user.save()
        error="NO"
      else:
        error="NOT"
    except:
      error="YES"

  return render(request, 'change_pass.html',locals())

#Change admin's Password
def changePassAdmin(request):
  if not request.user.is_authenticated:
    return redirect("adminLogin")
  error=""
  user=request.user

  if request.method=="POST":
    current=request.POST['currentPass']
    new=request.POST['newPass']

    try:
      if user.check_password(current):
        user.set_password(new)
        user.save()
        error="NO"
      else:
        error="NOT"
    except:
      error="YES"

  return render(request, 'admin/adminChange_pass.html',locals())

#showAllemployees
def allEmps(request):
  if not request.user.is_authenticated:
    return redirect('admin_login')

  employee=employeeDetails.objects.all()
  return render(request,'admin/allEmployees.html',{'employee':employee})

#delete Employees
def delete_emps(request,pid):
  if not request.user.is_authenticated:
    return redirect('admin_login')
  user=User.objects.get(id=pid)
  user.delete()
  return redirect('allEmps')

