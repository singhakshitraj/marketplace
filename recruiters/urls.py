from django.urls import path
from .views import *
urlpatterns = [
    path('',view=dashboard,name='Recruiter Dashboard'),
    path('login/',view=login_,name='Recruiter Login Page'),
    path('logout/',view=logout_,name='Recruiter Logout Page'),
    path('register/',view=register_,name='Recruiter Register Page'),
    path('add/',view=createJob,name='Create Job'),
    path('description/<str:id>/',view=job_description,name='Recruiter Job Description'),
    path('myprofile/',view=myProfile,name='Recruiter Profile')
]
