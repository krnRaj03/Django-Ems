import os
from email.errors import MessageError
from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout

#for e-mail
from django.core.mail import send_mail
from django.conf import settings
from requests import request

#models
from .models import *
from django.contrib import messages

#for pdfs
from django.http import FileResponse
import io
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4,LEGAL, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

#for text files
from django.http import HttpResponse
from fpdf import FPDF
from datetime import date

today = date.today()
now1=today.isoformat()
#grant Leave1 PDF
def grant_leave1(request,pid):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  user=User.objects.get(id=pid)
  employee=employeeDetails.objects.get(user=user)
  pdf = FPDF('P','mm','Letter')
  pdf.add_font('Arial','', r"C:\Windows\Fonts\arial.ttf", uni = True)

  pdf.add_page()
  # pdf.set_text_color(94, 107, 181)

  pdf.set_font('Arial', '',16)
  pdf.cell(0,10,'Bakı şəhəri', align='L')
  pdf.set_font('Arial', '',14)
  pdf.cell(0,10,txt=now1,ln=True, align='R')
  pdf.ln(7)
  ###
  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'“Xidməti zərurət ilə əlaqədar-\nezamiyyənin verilməsi barədə”', border = 0, 
                  align='R',ln=True)
  pdf.ln(7) 
  pdf.set_font('Arial', '',16)               
  pdf.cell(0,10,'ƏMR № 1/E',ln=1, align='C')
  pdf.ln(10)

  pdf.set_font('Arial', '',16)  
  pdf.cell(5,16,txt=employee.user.first_name, align='L')
  pdf.set_font('Arial', '',12)    
  pdf.cell(0,7,'Cəmiyyətin maliyyə şöbəsinin əməkdaşı, mühasib',ln=1, align='R')
  pdf.cell(0,7,'03.06.2022 -ci il tarixindən 15.06.2022 -ci il tarixinədək',ln=1, align='R')
  pdf.cell(0,7,'13 təqvim günü müddətinə İstanbul ezam edilsin.',ln=1, align='R')
  pdf.cell(0,7,'Mühasibatlıq şöbəsinə tapşırılsın ki, ezamiyyənin',ln=1, align='R')
  pdf.cell(0,7,'maliyyə təminatı ilə bağlı məsələləri',ln=1, align='R')
  pdf.cell(0,7,'qanunvericilikdə nəzərdə tutulmuş qaydada həll etsin.',ln=1, align='R')
  pdf.cell(0,7,'Əmrlə aidiyyatı şəxslər tanış edilsin.',ln=1, align='R')
  ###
  pdf.ln(16)
  pdf.set_font('Arial', '',14)
  pdf.cell(0,16,'Baş direktor', align='L')
  pdf.cell(0,7,'Vüsal Şərifov',ln=1, align='R')
  pdf.output("Employee Leave1.pdf")
  return FileResponse(open('Employee Leave1.pdf', 'rb'),as_attachment=True,content_type='application/pdf')

#grant Leave PDF
def grant_leave(request,pid):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  user=User.objects.get(id=pid)
  employee=employeeDetails.objects.get(user=user)

  class PDF(FPDF):
    def header(self):
      self.image('1.png', 90,8,30,25,30)
      self.ln(20)
      pdf.add_font('Arial','', r"C:\Windows\Fonts\arial.ttf", uni = True)
      pdf.set_font('Arial', '',20)
      self.cell(0,20,'EZAMİYYƏT VƏSİQƏSİ', align='C', ln=True)
        

  pdf = PDF('P','mm','Letter')
  pdf.add_font('Arial','', r"C:\Windows\Fonts\arial.ttf", uni = True)

  pdf.add_page()
      # pdf.set_text_color(94, 107, 181)

  pdf.set_font('Arial', '',12)
  pdf.cell(0,10,'№ 5/E', ln=True, align='C')
  pdf.ln(10)

  pdf.set_font('Arial', '',18)
  pdf.cell(0,10,txt=employee.user.first_name,ln=True, align='C')
  pdf.line(20,78,190,78)
  pdf.set_font('Arial', '',12)
  pdf.cell(0,10,'(soyadı, adı, atasının adı)',ln=True, align='C')
  pdf.ln(7)
      ###
  pdf.set_font('Arial', '',18)
  pdf.cell(0,10,txt=employee.designation,ln=True, align='C')
  pdf.line(20,107,190,107)
  pdf.set_font('Arial', '',12)
  pdf.cell(0,10,'(şöbə/bölmə, vəzifəsi)',ln=True, align='C')
  pdf.ln(7)
      ###
  pdf.set_font('Arial', '',18)
  pdf.cell(0,10,'“MAS” MMC, Bakı şəhəri',ln=True, align='C')
  pdf.line(20,134,190,134)
  pdf.set_font('Arial', '',12)
  pdf.cell(0,10,'(ezam olunduğu təşkilatın adı, ünvanı)',ln=True, align='C')
  pdf.ln(7)
      ###
  pdf.set_font('Arial', '',18)
  pdf.cell(0,10,'Xidməti zərurətlə bağlı',ln=True, align='C')
  pdf.line(20,160,190,160)
  pdf.set_font('Arial', '',12)
  pdf.cell(0,10,'(ezamiyyətin məqsədi)',ln=True, align='C')
  pdf.ln(7)
      ###
  pdf.set_font('Arial', '',18)
  pdf.cell(0,10,'Gəncə',ln=True, align='C')
  pdf.line(20,187,190,187)
  pdf.set_font('Arial', '',12)
  pdf.cell(0,10,'(təyinat məntəqəsi)',ln=True, align='C')
  pdf.ln(7)
      ###
  pdf.set_font('Arial', '',16)
  pdf.cell(0,10,'” 11 ”  gün müddətinə (yolda olduğu vaxt nəzərə alınmadan) ezam olunur.  ',ln=True)
  pdf.ln(10)
      ###
  pdf.set_font('Arial', '',16)
  pdf.cell(0,10,'Şəxsiyyəti təsdiq edən sənəd təqdim edildikdə etibarlıdır.',ln=True)
  pdf.ln(7)

  pdf.output("Employee Leave.pdf")
  return FileResponse(open('Employee Leave.pdf', 'rb'),as_attachment=True,content_type='application/pdf')


def pdf_gen(request):
  if not request.user.is_authenticated:
    return redirect('admin_login')

  employee=employeeDetails.objects.all()
  return render(request,'admin/pdfs.html',{'employee':employee})

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

  user=request.user
  empImage=employeeImage.objects.get(user=user)
  return render(request,'emp/emp_home.html',{'empImage':empImage})


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
  empImage=employeeImage.objects.get(user=user)
  if request.method=="POST":
    fn=request.POST['firstname']
    ln=request.POST['lastname']
    ec=request.POST['empcode']
    dept=request.POST['department']
    desig=request.POST['designation']
    cont=request.POST['contact']
    joindate=request.POST['jdate']
    gender=request.POST['gender']
    # eI=request.POST['image']

    # updating user data
    employee.first_name=fn
    employee.last_name=ln
    employee.empcode=ec
    employee.empdept=dept
    employee.designation=desig
    employee.contact=cont
    employee.gender=gender
    # empImage.image=eI

    if joindate:
      employee.join_date=joindate

    try:
      employee.save()
      employee.user.save()
      error="NO"
    except:
      error="YES"
  return render(request,'profile.html',locals())

#empImage
def emp_image(request,pid):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  error=''
  user=User.objects.get(id=pid)
  empImage=employeeImage.objects.get(user=user)

  if request.method=="POST":
    #taking a post request
    empImageUpload=request.POST['image']
    #storing the post request
    empImage.image=empImageUpload
    try:
      empImage.save()
      empImage.user.save()
      error="NO"
    except:
      error="YES"
  return render (request,'admin/upload_empImage.html' ,{'empImage':empImage})

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

