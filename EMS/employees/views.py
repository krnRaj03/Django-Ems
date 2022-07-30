import os
from email.errors import MessageError
from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
# from django.http import HttpResponse

#for e-mail
from django.core.mail import send_mail

#models
from .models import *
from django.contrib import messages

#for pdfs
from django.http import FileResponse
from fpdf import FPDF
from datetime import date

#for importing data
from .resources import empDetailsResource
from tablib import Dataset

today = date.today()
now1=today.isoformat()

###
def applyLeave(request):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  error=""
  user=request.user
  leave=employeeLeave.objects.get(user=user)
  print(leave)
  if request.method=="POST":
    #Company1 Profile
    #P.S the name in [] & is same as Models & same as HTML name tags
    typeoflea=request.POST['typeOfLeave']
    begdate=request.POST['beginDate']
    b1=begdate
    enddate=request.POST['endDate']
    print(enddate)
    totdays=request.POST['totalDays']
    reason=request.POST['commentsReasons']

    # updating user data
    #company1
    leave.typeOfLeave=typeoflea
    leave.beginDate=begdate
    leave.endDate=enddate
    leave.totalDays=totdays
    leave.commentsReasons=reason

    try:
      leave.save()
      leave.user.save()
      error="NO"
    except:
      error="YES"
  return render (request,'leaves/empApplyLeave.html')

def approveLeave(request,pid):
  if not request.user.is_authenticated:
    return redirect("emp_login")
  
  user=User.objects.get(id=pid)
  leave=employeeLeave.objects.get(user=user)
  print(leave)
  return render(request,'leaves/adminApproveLeave.html',{'leave':leave})

#for importing data
def simple_upload(request):
  if request.method=='POST':
      empDetail_resource=empDetailsResource()
      dataset=Dataset()
      new_employee=request.FILES['myfile']

      if not new_employee.name.endswith('xlsx'):
        messages.info(request,'wrong format!')
        return render(request,'upload.html')
      
      imported_data = dataset.load(new_employee.read(),format='xlsx')
      for data in imported_data:
        value= employeeDetails(
          data[0],
          data[1],
          data[2],
          data[3],
          data[4],
          data[5],
          data[6],
        )
        value.save()
  return render(request, 'admin/upload.html')

#Home Page
def home(request):
  return render(request,'index.html')

#Admin Login
def adminLogin(request):
  if request.method=="POST":
    u=request.POST['username']
    p=request.POST['pass1']
    user=authenticate(username=u, password=p)
    if user is not None and user.is_active:
      login(request,user)
      error="NO"
    else:
      error="YES"
  return render(request,'admin/admin_login.html',locals())

#Admin Home
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

#Display Employee Profile
def basicDetails(request):
  if not request.user.is_authenticated:
    return redirect("emp_login")

  user=request.user
  details=employeeDetails.objects.get(user=user)
  empImage=employeeImage.objects.get(user=user)
  return render(request,'emp/basic_profile.html',{'details':details,'empImage':empImage})

#Display Employee Experience
def myExp(request):
  if not request.user.is_authenticated:
    return redirect("emp_login")

  user=request.user
  experience=employeeExperience.objects.get(user=user)
  return render(request,'emp/my_exp.html',{'experience':experience})

#Display Employee Education
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
      employeeImage.objects.create(user=user)
      employeeLeave.objects.create(user=user)

      send_mail(
      'TEST Msg. from HR:',
      "Hi! Welcome to our company. ",
      'krnraj002@gmail.com',
      [user],
    )

      error="NO"
    except:
      error="YES"
  return render(request,'registration.html',locals())

#Employee Profile
def profile(request,pid):
  if not request.user.is_authenticated:
    return redirect("emp_login")
  error=''
  user=User.objects.get(id=pid)
  employee=employeeDetails.objects.get(user=user)
  # empImage=employeeImage.objects.get(user=user)
  if request.method=="POST":
    fn=request.POST['firstname']
    ln=request.POST['lastname']
    ec=request.POST['empcode']
    dept=request.POST['department']
    desig=request.POST['designation']
    cont=request.POST['contact']
    joindate=request.POST['join_date']
    gender=request.POST['gender']
    fathern=request.POST['fathersname']
    fin=request.POST['FIN']
    ssn=request.POST['SSN']
    passp=request.POST['passport']
    # eI=request.POST['image']

    # updating user data
    employee.first_name=fn
    employee.last_name=ln
    employee.empcode=ec
    employee.empdept=dept
    employee.designation=desig
    employee.contact=cont
    employee.gender=gender
    employee.fathersname=fathern
    employee.FIN=fin
    employee.SSN=ssn
    employee.passport=passp
    
    # empImage.image=eI

    if joindate:
      employee.join_date=joindate

    try:
      employee.save()
      employee.user.save()
      error="NO"
    except:
      error="YES"
  return render(request,'admin/profile.html',locals())

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

#Employee editable Education
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

#Change employee Password
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
  return redirect('deleteEmpPage')

def deleteEmpPage(request):
  if not request.user.is_authenticated:
    return redirect('admin_login')

  employee=employeeDetails.objects.all()
  # return render(request,'admin/allEmployees.html',{'employee':employee})
  return render(request,'admin/delete_emps.html',{'employee':employee})

#Employee Salaries
def emp_salary(request):
  return render(request,'admin/emp_sal.html')

###All PDFs

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

###Contarct gen
def contract_gen(request,pid):
  if not request.user.is_authenticated:
    return redirect("admin_login")
  user=User.objects.get(id=pid)
  employee=employeeDetails.objects.get(user=user)
  pdf = FPDF('P','mm','A4')
  pdf.add_font('Arial','', r"C:\Windows\Fonts\arial.ttf", uni = True)

  pdf.add_page()

  # 1st PART

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'Azərbaycan\n Respublikasının\n Əmək Məcəlləsinə\n 1-ci əlavə', align='R', ln=True)


  pdf.set_font('Arial', '',16)
  pdf.cell(0,12,'Əmək müqaviləsinin (kontraktının) nümunəvi forması', align='C', ln=True)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,10,'§1. Əmək müqaviləsini (kontraktının) bağlayan tərəflər haqqında məlumatlar ', ln=True, align='C')
  pdf.ln(10)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'1.1. Bu Əmək müqaviləsi (kontraktı), (bundan sonra ismin müvafiq halında «Əmək müqaviləsi») \nişəgötürənin səlahiyyətlərini həyata keçirən _____________________________________________ ', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,7,"(idarənin, müəssisənin, təşkilatın adı)",ln=True, align='R')

  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'İşəgötürəni __________________________________________________________________ ', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,7,"(idarənin, müəssisənin, təşkilatın adı)",ln=True, align='C')    

  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'___________________________________________________________________________ ilə  ', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,7,"(adı, atasının adı və soyadı) ",ln=True, align='C')    

  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'İşçi __________________________________________________________________________  ', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,7,"(adı, atasının adı və soyadı) ",ln=True, align='C')   


  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'________________________________________________________________________________  ', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,7,"(vətəndaşlığı, şəxsiyyətini təsdiq edən sənəd, onun nömrəsi, verildiyi tarix və onu verən orqanın adı)  ",ln=True, align='C') 


  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'________________________________________________________________________ arasında', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,7,"(təhsili, ixtisası, sənəti, peşəsi, bitirdiyi təhsil müəssisəsinin adı)",ln=True, align='C')   


  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'________________________________________________________________________ arasında', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,7,"(təhsili, ixtisası, sənəti, peşəsi, bitirdiyi təhsil müəssisəsinin adı)",ln=True, align='C') 
  pdf.ln(5)


  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'«___»____________ _____il tarixində Azərbaycan Respublikasının Əmək Məcəlləsinə (bundan  \nsonra "Əmək Məcəlləsi") müvafiq olaraq bağlanmışdır.', border = 0, 
                    align='L',ln=True)
  pdf.ln(5)


  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'1.2. İşçi __________________________________ vəzifəsinə (peşəsinə), işə qəbul (təyin) edilir. ', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,"(iş yerinin və vəzifənin, peşənin adı)",ln=True, align='L')
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'1.3. Bu Əmək müqaviləsi bağlanan gündən yaranmış əmək münasibətləri, tərəflərin hüquqları,\nvəzifələri və məsuliyyəti Əmək Məcəlləsi ilə müəyyən edilmiş qaydalarla və prinsiplərlə\ntənzimlənir. ', border = 0, 
                    align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',13)
  pdf.cell(0,7,'§2. Əmək müqaviləsinin müddəti  ', border = 0, 
                    align='L',ln=True)
  pdf.ln(3)


  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'2.1. Bu Əmək müqaviləsi müddətsiz bağlanmışdır ____________________________ ', border = 0, 
                    align='L',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,"(hə, yox)",ln=True, align='R')

  pdf.ln(7)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'2.2. İşin birinci ________həftəsi (ayı) sınaq müddəti hesab edilir. Sınaq müddəti ərzində tərəflərdən\nbiri digərini _______gün əvvəl xəbərdarlıq etməklə Əmək müqaviləsini birtərəfli qaydada poza\n bilər.', border = 0, 
                    align='L',ln=True)
  pdf.ln(5)


  # 2nd PAGE
  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'2.3. Bu Əmək müqaviləsi __________________________ səbəbə görə «___»________________ \n_____il tarixindən «___»_______________ ______il tarixinədək _____il (ay) müddətinə \n bağlanmışdır.', border = 0, 
                    align='L',ln=True)
  pdf.ln(3)

  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'2.4. İşçi «___»________________ _____il tarixindən işə başlayır.',align='L',ln=True)
  pdf.ln(7)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§3. İşçinin əmək funksiyası ',align='L',ln=True)
  pdf.ln(3)

  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'3.1. İşçi aşağıdakı əmək funksiyasının icrasını öhdəsinə götürür:',align='L',ln=True)
  pdf.ln(2)
  pdf.cell(0,7,'a) ___________________________________________________________________________;',align='L',ln=True)
  pdf.ln(2)
  pdf.cell(0,7,'b) ___________________________________________________________________________;',align='L',ln=True)
  pdf.ln(2)
  pdf.cell(0,7,'c) ___________________________________________________________________________;',align='L',ln=True)
  pdf.ln(2)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,'(əmək funksiyası tam təfsilatı ilə sadalanmalıdır) ',align='C',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'3.2. Bu əmək funksiyasından hər hansı birinin və ya bir neçəsinin dəyişdirilməsinə, habelə onlara \n əlavə funksiyanın daxil edilməsinə yalnız tərəflərin razılığı ilə yol verilir.',align='L',ln=True)
  pdf.ln(5)
  pdf.multi_cell(0,7,'3.3. İşçi Əmək Məcəlləsinin 10-cu maddəsi ilə müəyyən edilmiş əsas vəzifələrinin və bu əmək \n funksiyasının vaxtında, keyfiyyətlə yerinə yetirilməsinə əməl etməlidir.',align='L',ln=True)
  pdf.ln(5)
  pdf.multi_cell(0,7,'3.4. İşçi əmək funksiyasının icrası zamanı işəgötürənin istehsal fəaliyyəti ilə bağlı özünün ixtiraları \n, səmərələşdirici təklifləri barədə dərhal ona məlumat verməlidir. İşəgötürən öz növbəsində həmin\n ixtiraların, işçinin müəlliflik hüququnun və mülkiyyətçinin mənafeyinin qorunması üçün konkret\n tədbirlər görməlidir.',align='L',ln=True)
  pdf.ln(7)

  pdf.set_font('Arial', '',14)
  pdf.multi_cell(0,7,'§4. Əmək şəraitinin şərtləri',align='L',ln=True)
  pdf.ln(2)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'İşəgötürən aşağıdakı əmək şəraiti yaradılmasını və onun şərtlərinin təmin olunmasını öhdəsinə\n götürür:',align='L',ln=True)
  pdf.ln(3)
  pdf.cell(0,7,'Əmək haqqı üzrə ',ln=True)
  pdf.ln(3)
  pdf.multi_cell(0,7,'4.1. İşçiyə hər ay ____________________________________________məbləğdə əmək haqqı \nödənilir.',align='L',ln=True)
  pdf.cell(0,5,'4.2. Əmək haqqı:',align='L',ln=True)
  pdf.multi_cell(170,4,'• _______________________________manat məbləğində tarif haqqından (vəzifə\nmaaşından);',align='R',ln=True)
  pdf.multi_cell(154,4,'•tarif haqqına (vəzifə maaşına) _______faizi miqdarda əlavədən ibarətdir.',align='R',ln=True)
  pdf.ln(2)
  pdf.multi_cell(0,7,'4.3. İşçiyə ___________________________məbləğdə __________________________mükafat verilir. ',align='L',ln=True)
  pdf.set_font('Arial', '',10)
  pdf.cell(0,3,"(aylıq, rüblük, illik)",ln=True, align='R')


  # 3rd PAGE
  pdf.set_font('Arial', '',12)
  pdf.cell(0,10,'4.4. İşçi əmək funksiyasını ____________________________________ əmək şəraitli iş yerində ',align='L',ln=True)
  # pdf.ln(1)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,'(zərərli, ağır, yeraltı və s.)',align='C',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.cell(0,7,'icra etdiyi üçün onun əmək haqqına ___________________________məbləğdə əlavə müəyyən',align='L',ln=True)
  pdf.cell(0,5,' edilir.',align='L',ln=True)
  pdf.ln(7)

  pdf.multi_cell(0,7,'4.5. İşçiyə iş vaxtından artıq vaxtda, istirahət, səsvermə, ümumxalq hüzn günü və iş günü hesab \n edilməyən bayram günlərində işlədikdə __________ məbləğdə və ya ________________ qayda ilə\n hesablanmış Əmək Məcəlləsində nəzərdə tutulandan artıq əlavə əmək haqqı verilir. ',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,7,'4.6. Əmək haqqı:',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'• həftədə bir dəfə __________________________________________________________; ',align='R',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,'(həftənin günü)',align='C',ln=True)
  pdf.ln(2)
  #
  pdf.set_font('Arial', '',12)
  pdf.cell(0,5,'• ayda iki dəfə _____________________________________________________________; ',align='R',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,'(ayın maaş verilən günləri)',align='C',ln=True)
  pdf.ln(2)
  #
  pdf.set_font('Arial', '',12)
  pdf.cell(0,5,'• ayda bir dəfə _____________________________________________________ ödənilir;  ',align='R',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,'(ayın günü)',align='C',ln=True)
  pdf.ln(2)
  #
  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'• əmək haqqı və digər ödənclər işçinin _________________________________ bankdakı\n hesabına köçürülür.  ',align='R',ln=True)
  pdf.set_font('Arial', '',8)
  pdf.cell(0,5,'(bankın adı)',align='R',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'4.7. Tərəflərin əmək haqqının ödənilməsi barədə razılığa gəldikləri digər şərtlər: __________\n _____________________________________________________________________________.',align='',ln=True)
  pdf.ln(7)

  pdf.multi_cell(0,5,'4.8. Əmək haqqından yalnız qanunvericiliklə müəyyən edilmiş hallarda və qaydada tutulmalara yol \n verilir. Həmin tutulmalar haqqında işçi qabaqcadan məlumatlandırılır.',align='',ln=True)
  pdf.ln(8)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,5,'Əməyin mühafizəsi üzrə ',align='L',ln=True)
  pdf.ln(8)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'4.9. İşçinin sağlamlığının, əməyinin mühafizəsinin təmin olunması üçün sanitariya və gigiyena\n normalarına cavab verən iş yeri və iş şəraiti yaradılır. ',align='L',ln=True)
  pdf.ln(7)
  pdf.cell(0,5,'4.10. İşçi ________________________ xüsusi mühafizə vasitələri ilə təmin edilir.',align='L',ln=True)
  pdf.ln(7)
  pdf.multi_cell(0,5,'4.11. İşçi zərərli amillərdən sağlamlığının mühafizəsi üçün xüsusi __________________\n ______________________________________________________ qida məhsulları ilə təmin edilir ',align='L',ln=True)
  pdf.ln(7)
  pdf.multi_cell(0,5,'4.12. İşçi əməyin mühafizəsi normaları ilə ______________________ bir dəfədən az olmayaraq \n təlim atlandırılır.',align='L',ln=True)
  pdf.ln(7)
  pdf.multi_cell(0,5,'4.13. İşçi özünün və iş yoldaşlarının həyatının və sağlamlığının qorunması üçün müəyyən edilmiş \n əməyin mühafizəsi qaydalarına və normalarına əməl etməyə borcludur.',align='L',ln=True)
  pdf.ln(14)

  #4th Page
  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'4.14. İşəgötürən istehsal qəzaları, peşə xəstəliyi nəticəsində işçiyə və ya onun himayəsində olan\n şəxslərə dəyən maddi ziyanı və digər xərcləri ödəyir.',align='L',ln=True)
  pdf.ln(5)
  pdf.multi_cell(0,5,'4.15. İşəgötürənin təqsiri üzündən əməyin mühafizəsi normaları və qaydaları pozulduğuna görə işçi \n həlak olarsa, onun himayəsində olan şəxslər qarşısında işəgötürən qanunvericilikdə nəzərdə tutulan qaydada maddi məsuliyyət daşıyır.',align='L',ln=True)
  pdf.ln(8)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,5,'İş və istirahət vaxtı üzrə ',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.cell(0,5,'4.16. İşçi gündə 8 saatdan, həftə ərzində isə 40 saatdan çox olmayaraq işləyir.',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'4.17. İş saat __________________ başlanır, saat ___________________ qurtarır.',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'4.18. Nahar vaxtı saat __________________-dan saat ___________________-dəkdir.',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'4.19. İşçi hər gün ___________________saat natamam iş günü işləyir.',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'4.20. İşçi həftədə ____________________gün natamam iş həftəsi ilə işləyir.',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'4.21. İş ____________________növbəlidir:',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(155,5,'• Birinci növbə saat ______________başlanır və saat ____________qurtarır. ',align='R',ln=True)
  pdf.ln(5)
  pdf.cell(155,5,'• İkinci növbə saat ______________başlanır və saat ____________qurtarır.  ',align='R',ln=True)
  pdf.ln(5)
  pdf.cell(159,5,'• Üçüncü növbə saat ______________başlanır və saat ____________qurtarır.  ',align='R',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'4.22. İşə gəlib getməsi üçün nəqliyyatla təmin edilir __________________________ ',align='L',ln=True)
  pdf.set_font('Arial', '',9)
  pdf.cell(0,5,'(hə, yox)',align='R',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.cell(0,5,'4.23. İstirahət günləri hər həftənin ______________________________ günləridir.',align='L',ln=True)
  pdf.ln(5)
  pdf.multi_cell(0,5,'4.24. İşçiyə iş vaxtından artıq işlərin yerinə yetirilməsinə görə qanunvericilikdə nəzərdə tutulan \n məbləğdən ___________ artıq məbləğdə haqq ödənilir;',align='L',ln=True)
  pdf.ln(5)
  pdf.multi_cell(0,5,'4.25. İşçi iş vaxtından kənar vaxtda və ya işəgötürənin razılığı ilə iş vaxtı ərzində işəgötürənlə \n rəqabətdə olmayan müəssisədə əlavə iş yerində əvəzçilik üzrə işləyə bilər.',align='L',ln=True)
  pdf.ln(8)
  pdf.set_font('Arial', '',14)
  pdf.cell(0,5,'Məzuniyyət üzrə ',align='L',ln=True)
  pdf.ln(8)

  pdf.set_font('Arial', '',12)
  pdf.cell(0,5,'4.26. İşçinin iş ilini __________________________________________________ aylardan ibarət ',align='L',ln=True)
  pdf.set_font('Arial', '',9)
  pdf.cell(0,5,'(birinci iş ili başlanan və bitən gün, ay və il)',align='R',ln=True)


  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'dövr əhatə edir və ona hər növbəti iş ili üçün müddəti Əmək Məcəlləsi ilə müəyyən edilmiş əmək\n məzuniyyəti verilir. ',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'4.27. Əsas məzuniyyətinin müddəti ______________________təqvim günüdür.',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(0,5,'4.28. Əlavə məzuniyyət müddəti:',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(136,5,'• əmək stajına görə _______________________təqvim günü; ',align='R',ln=True)
  pdf.ln(2)
  pdf.cell(155,5,'•əmək şəraitinin xarakterinə görə ____________________ təqvim günü; ',align='R',ln=True)
  pdf.ln(2)


  ### Page 5
  pdf.cell(170,5,'•14 yaşadək ikidən çox uşağı olan qadına ___________________ təqvim günü;  ',align='R',ln=True)
  pdf.ln(2)
  pdf.cell(152,5,'•kollektiv müqavilə (saziş) üzrə ____________________ təqvim günü.  ',align='R',ln=True)
  pdf.ln(8)


  pdf.cell(0,5,'4.29. Əmək məzuniyyətinin ümumi müddəti ____________________ təqvim günü.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'4.30. Əmək məzuniyyətinə çıxarkən:',align='L',ln=True)
  pdf.ln(5)
  pdf.cell(170,5,'• _____________________________ məbləğdə sosial-məişət müavinəti verilir; ',align='R',ln=True)
  pdf.ln(2)
  pdf.multi_cell(170,5,'• bundan savayı sanatoriya-kurort müalicəsi, turizm səfərlərinə getməsi, məzuniyyətin \ndaha mənalı keçirilməsi üçün __________________________________ tədbirlər görülür. ',align='R',ln=True)
  pdf.set_font('Arial', '',9)
  pdf.cell(0,3,'(konkret tədbir və ya pul ödənci)',align='R',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'4.31. Təhsil almaqla əlaqədar ödənişli məzuniyyətlər Əmək Məcəlləsində nəzərdə tutulan müddətdə\n verilir və işəgötürən bununla yanaşı işçinin təhsilini artırmaq üçün zəruri tədbirləri görməyi öhdəsinə\n götürür.',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,5,'4.32. Ödənişsiz məzuniyyətdən Əmək Məcəlləsi ilə müəyyən edilmiş hallarda, habelə işəgötürənlə \n razılıq əsasında istifadə edilir.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'Tərəflərin müəyyən etdiyi, habelə kollektiv müqavilədə (sazişdə) nəzərdə tutulan digər əlavə şərtlər',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'4.33. _________________________________________________________________________.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'4.34. _________________________________________________________________________.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'4.35. _________________________________________________________________________.',align='L',ln=True)
  pdf.ln(2)

  pdf.set_font('Arial', '',9)
  pdf.cell(0,3,'(bütün əlavə şərtlər təfsilatı ilə sadalanmalıdır).',align='C',ln=True)
  pdf.ln(8)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,3,'Bədən tərbiyəsi və idman üzrə ',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'4.36. İşçiyə bədən tərbiyəsi və idmanla, o cümlədən iş rejimi şəraitində və işdən sonrakı\n reabilitasiya və peşəkar-tətbiqi məşqlərlə, idman-sağlamlıq turizmi ilə məşğul ola bilməsi üçün\n şərait yaradılır. ',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,5,'4.37. İşçinin bədən tərbiyəsi və idman şəraiti məsələləri üzrə şərtlər:\n ____________________________________________________________.',align='L',ln=True)
  pdf.ln(7)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§5. Birinin digərinə vurduğu ziyana görə tərəflərin qarşılıqlı maddi məsuliyyəti ',align='L',ln=True)
  pdf.ln(8)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'5.1. Bu Əmək müqaviləsinin tərəflərindən biri digərinin əmlakına, səhhətinə, maddi, istehsal,\n kommersiya maraqlarına, qanunla qorunan mənafelərinə ziyan vurarsa, digər tərəf qarşısında\n qanunvericiliklə müəyyən olunmuş qaydada maddi və mənəvi məsuliyyət daşıyır.',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'5.2. Tərəflər istehsal və icra riski istisna olmaqla biri digərinə ziyan vurarsa, dəyən zərəri könüllü\n şəkildə digər tərəfə ödəməyi öhdəsinə götürürlər. Əgər bir tərəf digər tərəfin hüquqlarını pozaraq\n qarşılıqlı şəkildə dəyən zərərin ödənilməsi razılığına gəlməzsə, ziyan dəyən tərəf məhkəmə\n qaydasında ziyanın ödənilməsini təmin etmək hüququna malikdir.',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'5.3. Tərəflər məhkəməyə müraciət etmədən ziyan vurmadan əmələ gələn öhdəliklərinin özləri\n tərəfindən həllinə üstünlük verirlər.',align='L',ln=True)
  pdf.ln(7)

  ###Page 6
  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§6. Sosial müdafiə məsələləri ',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'6.1. İşçinin məcburi dövlət sosial sığortası üçün qanunvericiliklə müəyyən olunmuş qaydada hər ay\n _________________________məbləğdə sığorta haqqı ödənilir və işəgötürən tərəfindən o,\n ____________________________ məbləğdə əlavə sığorta edilir.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,7,'6.2. İşçinin sosial müdafiə olunması, güzəşt və imtiyazları, sosial sığorta hüququ təmin edilir.',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,5,'6.3. İşçiyə əmək qabiliyyətinin müvəqqəti itirilməsi ilə əlaqədar qanunvericiliklə müəyyən edilmiş\n qaydada və məbləğdə müavinət verilir.',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§7. Mülkiyyət münasibətlərinin tənzimlənməsi ',align='L',ln=True)
  pdf.ln(8)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'7.1. İşçi iş vaxtı ərzində həm onun bilavasitə istifadəsinə verilən, həm də başqa istehsal vasitələrinin\n — maşın, mexanizm, avadanlıq, cihaz və alətlərin, qurğu, habelə işəgötürənin mülkiyyətində olan\n digər əmlakın qorunmasına cavabdehdir.',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,5,'7.2. İşçinin müəssisənin mülkiyyətində _____________________ qədər payı var və işəgötürənlə\n mülkiyyət münasibətləri həmin paya mütənasib olaraq qanunvericiliklə müəyyən edilən qaydada\n tənzimlənir.',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,5,'7.3. İşçi müəssisənin mülkiyyətindəki payına görə nizamnamə ilə müəyyən edilən _____________\n məbləğdə dividend almaq hüququna malikdir.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'7.4. İşçi əmək funksiyasının icrası zamanı özünün aşağıdakı şəxsi əmlakından istifadə edir:',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'a) ____________________________________________________________________________;',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'b) ____________________________________________________________________________.',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,5,'7.5. İşəgötürən işçinin əmlakının mühafizəsinə və aşınmasına görə əvəzinin ödənilməsinə\n cavabdehdir.',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,5,'7.6. İşçi işəgötürənin kommersiya və istehsal sirrinin qorunmasına cavabdehdir və bu sirləri\n yaymağa görə qanunvericilikdə və bu Əmək müqaviləsində nəzərdə tutulan məsuliyyət daşıyır.',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§8. Əmək müqaviləsinə dəyişikliklər və əlavələr edilməsi barədə məlumatlar',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'8.1. Bu Əmək müqaviləsinə birtərəfli qaydada aparılmış dəyişikliklərin, əlavələrin, düzəlişlərin \n hüquqi qüvvəsi yoxdur.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,7,'8.2. Bu Əmək müqaviləsinə aşağıdakı dəyişikliklər, əlavələr edilmişdir:',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'a) ____________________________________________________________________________;',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'b) ____________________________________________________________________________;',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,5,'c) ____________________________________________________________________________.',align='L',ln=True)
  pdf.ln(8)

  ###Page7
  pdf.set_font('Arial', '',9)
  pdf.cell(0,3,'(bütün dəyişikliklər və əlavələr təfsilatı ilə sadalanmalıdır).',align='C',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,5,'8.3. Tərəfimizdən razılaşdırılmış dəyişikliklər və əlavələr dərhal (_____________ gündən gec\n olmayaraq) qüvvəyə minir və bu Əmək müqaviləsinin tərkib hissəsini təşkil edir.',align='L',ln=True)
  pdf.ln(3)

  pdf.cell(0,5,'İmzalar: ',align='L',ln=True)
  pdf.ln(3)

  pdf.cell(0,5,'___________________________________ İşəgötürən',align='L',ln=True)
  pdf.ln(3)
  pdf.cell(0,5,'___________________________________ İşçi',align='L',ln=True)
  pdf.ln(3)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§9. Əmək müqaviləsinə xitam verilməsi ',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'9.1. Bu Əmək müqaviləsi Əmək Məcəlləsinin 68, 69, 70, 73, 74 və 75-ci maddələrində nəzərdə\n tutulan əsaslarla və qaydalara ciddi əməl olunmaqla tərəflərin birinin təşəbbüsü ilə ləğv edilə bilər.',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'9.2. İşəgötürən tərəfindən bu Əmək müqaviləsi ləğv edilərkən işçi qanunvericilikdə nəzərdə tutulan\n hallarda xəbərdar edilir.',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'9.3. İşçi tərəfindən bu əmək müqaviləsi ləğv edilməzdən əvvəl işəgötürən bir təqvim ayı\n qabaqcadan xəbərdar edilməlidir.',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'9.4. İşəgötürən tərəfindən zor işlədilərək, hədə-qorxu gələrək, yaxud hər hansı başqa üsulla işçinin\n iradəsinin əleyhinə bu Əmək müqaviləsini ləğv etməyə onun məcbur edilməsinə yol verilmir.',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,7,'9.5. Əmək müqaviləsinə xitam verilməsi barədə tərəflərin müəyyən etdiyi hallar:',align='L',ln=True)
  pdf.ln(3)

  pdf.multi_cell(0,7,'_______________________________________________________________________________\n _______________________________________________________________________________\n _______________________________________________________________________________',align='L',ln=True)
  pdf.ln(3)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§10. Yekun qaydalari ',align='L',ln=True)
  pdf.ln(3)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'10.1. Bu Əmək müqaviləsinin qüvvədə olduğu müddət ərzində tərəflər yaranan əmək\n mübahisələrinin həllinə qarşılıqlı anlaşma və razılıq yolu ilə biri digərinin hüquqlarını pozmadan nail olacaqlar. Tərəflər əmək mübahisələrinin həlli haqqında razılığa gəlmədikdə mübahisənin\n məhkəmə qaydasında araşdırılması hüququndan istifadə edəcəklər.',align='L',ln=True)
  pdf.ln(3)
  pdf.multi_cell(0,7,'10.2. Bu Əmək müqaviləsi iki nüsxədə tərtib edilib, onlardan biri işçidə, digəri isə işəgötürəndə\n saxlanılır.',align='L',ln=True)
  pdf.ln(3)
  pdf.multi_cell(0,7,'10.3. Tərəflər bu Əmək müqaviləsi üzrə öhdəliklərinin icrasını üçüncü şəxslərə həvalə edə\n bilməzlər.',align='L',ln=True)
  pdf.ln(3)
  pdf.multi_cell(0,7,'10.4. Tərəflər bu Əmək müqaviləsi ilə nəzərdə tutulmamış, habelə bilavasitə Əmək Məcəlləsi ilə\n müəyyən edilən hallar istisna olunmaqla, üçüncü şəxslər qarşısında biri digərinin öhdəliklərinə görə\n cavabdehlik daşımırlar.',align='L',ln=True)
  pdf.ln(3)
  pdf.multi_cell(0,7,'10.5. Tərəflər bu Əmək müqaviləsinin şərtlərini, Əmək Məcəlləsi ilə müəyyən edilən vəzifələrini\n, habelə biri digərinin qanuni mənafelərini və hüquqlarını pozarsa, təqsirkar tərəfin məsuliyyətə cəlb\n edilməsini müvafiq dövlət orqanlarından, mülkiyyətçidən tələb etmək hüququna malikdirlər.',align='L',ln=True)
  pdf.ln(3)

  pdf.multi_cell(0,7,'10.6. Bu Əmək müqaviləsinin şərtlərini, bu şərtlərdən irəli gələn öhdəliklərimizi vicdanla yerinə\n yetirəcək, şəxsi, maddi, maliyyə, istehsal maraqlarımıza, habelə ictimai birliklərdə və siyasi\n partiyalarda müstəqil iştirakımıza qarşılıqlı hörmət göstərəcəyik.',align='L',ln=True)
  pdf.ln(3)

  pdf.set_font('Arial', '',14)
  pdf.cell(0,7,'§11. Tərəflərin imzaları və ünvanları ',align='L',ln=True)
  pdf.ln(5)

  pdf.set_font('Arial', '',12)
  pdf.multi_cell(0,7,'11.1. İşəgötürənin vəzifəsi, adı, atasının adı və soyadı, habelə müştərisi olduğu bankın adı,\n hesablaşma hesablarının nömrələri, kodu, sahibkarlıq fəaliyyəti ilə məşğul olmağa hüquq verən\n xüsusi razılığın məlumatları göstərilməklə hüquqi ünvanı:',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,7,'Möhürü                    	İmzası:',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,7,'11.2. İşçinin adı, atasının adı və soyadı göstərilməklə ünvanı:',align='L',ln=True)
  pdf.ln(5)

  pdf.cell(0,7,'İmzası:	                    Tarix:',align='L',ln=True)
  pdf.ln(5)

  pdf.multi_cell(0,7,'Qeyd: Əmək Məcəlləsinin 43-cü maddəsində nəzərdə tutulan Əmək müqaviləsinin məzmununa\n daxil olan şərtlər, məlumatlar həmin müqavilə tərtib edilərkən hökmən göstərilməlidir. Bu\n nümunədə göstərilən əlavə müddəaların, şərtlərin hər biri konkret hallarda işəgötürən və işçi\n tərəfindən Əmək müqaviləsi bağlanarkən razılaşdırılaraq tərtib edilir. Lakin bütün hallarda\n işəgötürən Əmək müqaviləsinin məzmununu bu nümunədə göstərilən qaydada dolğun şəkildə tərtib\n etməyə borcludur. İşəgötürən bu nümunəyə tam uyğun olan Əmək müqaviləsinin formalarının\n kifayət miqdarda nəşriyyat üsulu ilə hazırlanmasını təmin etməlidir. Əmək müqaviləsinin\n formasındakı boş yerlər əl ilə və ya makinada, kompüterdə səliqə ilə yazılmalıdır, məlumatların\n pozulmasına, qaralanmasına yol verilməməlidir.',align='L',ln=True)
  pdf.ln(16)

  pdf.multi_cell(0,7,'* Bu sənəd tərəflərin iradəsindən asılı olaraq eyni hüquqi məna kəsb edən «Əmək müqaviləsi» və\n ya «Əmək kontraktı» formasında tərtib edilir.',align='L',ln=True)


  pdf.output("Employee Contract.pdf")
  return FileResponse(open('Employee Contract.pdf', 'rb'),as_attachment=True,content_type='application/pdf')
  
def pdf_gen(request):
  if not request.user.is_authenticated:
    return redirect('admin_login')

  employee=employeeDetails.objects.all()
  return render(request,'admin/pdfs.html',{'employee':employee})