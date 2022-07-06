from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    #all Admin urls
    path('admin_login', views.adminLogin, name="adminLogin"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('all_employees', views.allEmps, name="allEmps"),
    path('change_passAdmin', views.changePassAdmin, name="changePassAdmin"),
    path('delete_employees/<int:pid>', views.delete_emps, name="delete_emps"),
    path('edit_profile/<int:pid>', views.edit_profile, name="edit_profile"),

    #all Emp urls
    path('registration', views.register, name="register"),
    path('emp_login', views.emp_login, name="emp_login"),
    path('emp_home', views.emp_home, name="emp_home"),
    path('profile', views.profile, name="profile"),
    path('logout', views.Logout, name="logout"),
    path('my_exp', views.myExp, name="myExp"),
    path('edit_exp', views.editExp, name="editExp"),
    path('my_edu', views.myEdu, name="myEdu"),
    path('edit_edu', views.editEdu, name="editEdu"),
    path('change_pass', views.changePass, name="changePass"),
    
]
