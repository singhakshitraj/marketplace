from django.shortcuts import render,redirect,get_object_or_404
from .models import Recruiter,Professions,TechStacks
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .exceptions import *
import os
from django.conf import settings
import markdown
from .utils import apply_middleware
from .middleware import CheckRecruiterAccountMiddleware
from django.conf.urls import handler404
from candidates.models import UserJobApplication
import requests
# Create your views here.

@login_required(login_url='/recruiter/login/')
@apply_middleware(CheckRecruiterAccountMiddleware)
def dashboard(request):
    rec = Recruiter.objects.get(user=request.user)
    professions = Professions.objects.filter(created_by=rec).order_by('created_at')
    context = {
        'professions':professions,
        'recruiter':rec
    }
    return render(request,'recruiter/recruiter_page.html',context=context)

def login_(request):
    context = dict()
    if request.method == 'POST':
        try:
            user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
            if user is None:
                raise IncorrectCredentials()
            recruiter_acc = Recruiter.objects.filter(user=user)
            if recruiter_acc is None:
                return Http404('Not A Valid Recruiter Account. Login as a recruiter to access this page')
            login(request=request,user=user)
            return redirect('Recruiter Dashboard')
        except IncorrectCredentials as exceptions:
            context['error_message'] = 'Incorrect Credentials'
        except Exception as exceptions: 
            context['error_message'] = exceptions
        context['form'] = RecruiterLoginForm(request.POST)
        return render(request,'registration/recruiter_login_page.html',context=context)
    else:
        context['form'] = RecruiterLoginForm()
    return render(request,'registration/recruiter_login_page.html',context=context)

def register_(request):
    context = dict()
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        try:
            rec = form.save(commit=True)
            login(request,user=rec.user)
            return redirect('Recruiter Dashboard')
        except Exception as exceptions:
            print(exceptions)
            context['error_message'] = exceptions
            return Http404(exceptions)
    else:
        context['form'] = RecruiterRegistrationForm()
    return render(request,'registration/recruiter_signup_page.html',context=context)

def logout_(request):
    try:
        logout(request)
        return redirect('Recruiter Dashboard')
    except Exception as exception:
        print(exception)
        return Http404(exception)
    
    
@login_required(login_url='/recruiter/login/')
@apply_middleware(CheckRecruiterAccountMiddleware)
def createJob(request):
    context = dict()
    if request.method == 'POST':
        form = CreateJobForm(request.POST,request.FILES)
        try:
            profession = form.save(request.user,commit=True)
            for i in form.cleaned_data['techstack']:
                profession.techstack.add(i)
            profession.save()
            return redirect('Recruiter Job Description',id=profession.id)
        except Exception as exception:
            context['error_message'] = exception
        context['form'] = CreateJobForm(request.POST,request.FILES)
        return render(request,'recruiter/add_profession.html',context=context)
    else:
        form = CreateJobForm()
        context['form'] = form
        context['all_tech_stacks'] = TechStacks.objects.all()
    return render(request,'recruiter/add_profession.html',context=context)

@login_required(login_url='/recruiter/login/')
@apply_middleware(CheckRecruiterAccountMiddleware)
def job_description(request,id):
    context = dict()
    job = get_object_or_404(Professions,id=id)
    file = requests.get(job.md_content.url)
    md_content = file.text
    context['html_format'] = markdown.markdown(md_content,extensions=['extra'])
    context['job'] = job
    if job.created_by == Recruiter.objects.get(user=request.user):
        context['applications'] = UserJobApplication.objects.filter(profession=job).order_by('-applied_at')
    print(context['applications'])
    return render(request,'recruiter/job_description.html',context=context)

@login_required(login_url='/recruiter/login/')
@apply_middleware(CheckRecruiterAccountMiddleware)
def myProfile(request):
    rec = Recruiter.objects.get(user=request.user)
    professions = Professions.objects.filter(created_by=rec).order_by('created_at')
    context = {
        'professions':professions,
        'recruiter':rec
    }
    return render(request,'recruiter/profile_page.html',context=context)