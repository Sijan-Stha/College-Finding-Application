from django.urls import path
from . import views



urlpatterns = [
    # Start Page or Home Page
    path('', views.home, name='homepage'),




    # For Login and Logout
    path('loginPage/', views.loginPage, name='loginPage'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),




    # For Registration
    path('signUp/', views.signUp, name='signUp'),
    path('student_registration/', views.student_registration, name='student_registration'),
    path('registerCollege/', views.registerCollege, name='registerCollege'),





    # For Student
    path('searchCollege/', views.searchCollege, name='searchCollege'),
    path('compareCollege/', views.compareCollege, name='compareCollege'),
    path('blogNews/', views.blogNews, name='blogNews'),
    path('collegeList/', views.collegeList, name='collegeList'),
    path('searchCollegeByName/', views.searchCollegeByName, name='searchCollegeByName'),
    path('studentViewCollegeProfile<int:org_id>', views.studentViewCollegeProfile, name='studentViewCollegeProfile'),
    path('bookAppointment/', views.bookAppointment, name='bookAppointment'),





    # For Colleges
    path('collegeHome/', views.collegeHome, name='collegeHome'),
    path('viewAppointment/', views.viewAppointment, name='viewAppointment'),
    path('updateAppointment/', views.updateAppointment, name='updateAppointment'),
    path('collegeProfile/', views.collegeProfile, name='collegeProfile'),
    path('editCollegeProfile/', views.editCollegeProfile, name='editCollegeProfile'),
    path('postBlog/', views.postBlog, name='postBlog'),
    path('deleteBlog<int:blog_id>', views.deleteBlog, name='deleteBlog'),





    # For Admin
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('adminLogout/', views.adminLogout, name='adminLogout'),
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),
    path('deleteBlogDashboard<int:blog_id>', views.deleteBlogDashboard, name='deleteBlogDashboard'),
    path('adminViewStudent/', views.adminViewStudent, name='adminViewStudent'),
    path('adminDeleteStudent<int:std_id><str:std_userName>', views.admin_delete_student, name='admin_delete_student'),
    path('adminViewCollege/', views.adminViewCollege, name='adminViewCollege'),
    path('admin_delete_college<int:org_id><str:cs_username>', views.admin_delete_college, name='admin_delete_college'),
    path('adminRegisterCollege/', views.adminRegisterCollege, name='adminRegisterCollege'),
    path('registerUnregisteredCollege<int:org_id><str:cs_username>', views.registerUnregisteredCollege,
         name='registerUnregisteredCollege'),
    path('admin_delete_unregisteredCollege<int:org_id>', views.admin_delete_unregisteredCollege, name='admin_delete_unregisteredCollege'),
    path('adminNews/', views.adminNews, name='adminNews'),
    path('deleteNews<int:news_id>', views.deleteNews, name='deleteNews'),






    # URLS FOR VIDEO COUNSELLING FEATURE
    path('lobby/', views.lobby, name = 'lobby'),
    path('room/', views.room, name = 'room'),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]