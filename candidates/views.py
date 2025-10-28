import markdown
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from recruiters.models import Professions
from .exceptions import AuthException, UserAlreadyExistsException
from .forms import JobApplicationForm, CandidateRegistrationForm, CustomAuthenticationForm
from .middleware import CheckCandidateAccountMiddleware
from .models import Candidates, UserJobApplication, BookmarkedJobs
from .utils import apply_middleware
from django.http import JsonResponse


def first_display_page(request):
    return render(request,'common/home_page.html')

def health_check(request):
    return JsonResponse({'status':'OK'})


@login_required(login_url='/login/')
@apply_middleware(CheckCandidateAccountMiddleware)
def dashboard(request):
    jobs = Professions.objects.all()[:20]
    return render(request,'candidate/candidate_page.html',context={'jobs':jobs})


@login_required(login_url='/login/')
@apply_middleware(CheckCandidateAccountMiddleware)
def job_description(request,id):
    job = get_object_or_404(Professions,id=id)
    file = requests.get(job.md_content.url)
    md_content = file.text
    html_format = markdown.markdown(md_content,extensions=['extra'])
    bflater = BookmarkedJobs.objects.filter(user=request.user,profession_id=id)
    application = UserJobApplication.objects.filter(
        candidate=Candidates.objects.get(user=request.user),
        profession=Professions.objects.get(pk=id)
    )
    applied = True if(len(application)!=0) else False
    if request.method == 'POST':
        if len(bflater)==0:
            new_bflater = BookmarkedJobs(user=request.user,profession_id=id)
            new_bflater.save()
            marked = True
        else:
            BookmarkedJobs.objects.filter(user=request.user,profession_id=id).delete()
            marked = False
    else:
        marked = True if(len(bflater)!=0) else False
    return render(request,'candidate/job_description.html',context={'details':job,'content':html_format,'marked':marked,'applied':applied})


@login_required(login_url='/login/')
@apply_middleware(CheckCandidateAccountMiddleware)
def applyNow(request,id):
    cand = Candidates.objects.get(user=request.user)
    proff = Professions.objects.get(pk=id)
    if request.method == 'POST':
        form_data = JobApplicationForm(request.POST)
        if form_data.is_valid():
            try:
                cl_data = form_data.clean()
                application = UserJobApplication(candidate=cand,profession=proff,get_hired=cl_data['get_hired'])
                application.save()
                return redirect('Dashboard')
            except BaseException as error:
                print(error)
                raise Http404(error)
        else:
            raise Http404('Unclean Data')
    else:
        form = JobApplicationForm()
        context = {
            'form':form,
            'profession':proff
        }
        return render(request,'candidate/apply_page.html',context=context)


@login_required(login_url='/login/')
@apply_middleware(CheckCandidateAccountMiddleware)
def myProfile(request):
    user = User.objects.get(username=request.user.username)
    cands = Candidates.objects.get(user = user)
    file = requests.get(cands.md_content.url)
    md_co = file.text
    file = requests.get(cands.resume.url)
    resu = file.text
    html_md_co = markdown.markdown(md_co,extensions=['extra'])
    html_resu = markdown.markdown(resu,extensions=['extra'])
    context = {
        'user': cands,
        'md_content':html_md_co,
        'resume' : html_resu
    }
    return render(request,'candidate/profile_page.html',context=context)

def login_(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request,username=username,password=password)
            if user is None:
                raise AuthException()
            login(request,user)
            return redirect('Dashboard')
        except AuthException as e:
            context['error_message'] = 'Auth Credentials error'
        except BaseException as e:
            print(e)
            return Http404(e)
        context['form'] = CustomAuthenticationForm(request.POST)
        return render(request,'registration/candidate_login_page.html',context=context)
    else:
        context['form'] = CustomAuthenticationForm()
    return render(request,'registration/candidate_login_page.html',context=context)

def register_(request):
    context = dict()
    if request.method == 'POST':
        candidate_form = CandidateRegistrationForm(request.POST,request.FILES)
        try:
            cands = candidate_form.save(commit=True)
            login(request,cands.user)
            return redirect('Dashboard')
        except UserAlreadyExistsException as userexists:
            context['error_message'] = userexists
        context['form'] = CandidateRegistrationForm(data=request.POST)
    else:
        context['form'] = CandidateRegistrationForm()
    return render(request,'registration/candidate_signup_page.html',context=context)


def logout_(request):
    try:
        logout(request)
        return redirect('Login Page')
    except Exception as e:
        print(e)
        raise Exception(e)

def formatterToExperience(request):
    return render(request,'common/exp_to_json.html')


@login_required(login_url='/login/')
@apply_middleware(CheckCandidateAccountMiddleware)
def getUserApplications(request):
    if request.user is None:
        raise Http404('User Login Failed')
    job_apps = UserJobApplication.objects.filter(candidate=Candidates.objects.get(user=request.user))
    return render(request,'candidate/my_applications.html',context={'applications':job_apps})


@login_required(login_url='/login/')
@apply_middleware(CheckCandidateAccountMiddleware)
def getBookmarks(request):
    if request.user is None:
        raise Http404('User Login Failed')
    bookmarks = BookmarkedJobs.objects.filter(user=request.user)
    return render(request,'candidate/bookmarks.html',context={'bookmarks':bookmarks})

def docs(request):
    return render(request,'common/docs.html')