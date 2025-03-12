from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('',view=views.first_display_page),
    path('dashboard/', view=views.dashboard,name='Dashboard'),
    path('apply/<str:id>/',view=views.applyNow,name='Apply Now'),
    path('description/<str:id>/',view=views.job_description,name='Job Description'),
    path('myprofile/',view=views.myProfile,name='My Profile'),
    path('login/',view=views.login_,name='Login Page'),
    path('register/',view=views.register_,name='SignUp Page'),
    path('formatter/',view=views.formatterToExperience,name='Formatter'),
    path('applications/',view=views.getUserApplications,name='Get User Applications'),
    path('bookmarks/',view=views.getBookmarks,name='Get Bookmarks'),
    path('logout/',view=views.logout_,name='Logout'),
    path('docs/',view=views.docs)
]
