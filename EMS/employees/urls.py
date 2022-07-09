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
    path('edit_exp/<int:pid>', views.editExp, name="editExp"),
    path('edit_edu/<int:pid>', views.editEdu, name="editEdu"),
    # path('update_profile/<int:pid>', views.update_emps, name="update_emps"),

    #all Emp urls
    path('registration', views.register, name="register"),
    path('emp_login', views.emp_login, name="emp_login"),
    path('emp_home', views.emp_home, name="emp_home"),
    path('profile', views.profile, name="profile"),
    path('logout', views.Logout, name="logout"),
    path('my_exp', views.myExp, name="myExp"),
    path('my_edu', views.myEdu, name="myEdu"),
    path('change_pass', views.changePass, name="changePass"),
    
]
