from typing import Any
from .models import Recruiter,Professions
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .exceptions import UserAlreadyExists,NotARecruiterAccount
from .models import TechStacks,PROFESSION_TYPE

class RecruiterRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'style':'width:100%;border-radius:3px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style':'width:100%;border-radius:3px;'}))
    class Meta:
        model = Recruiter
        fields = ['name','description']
        widgets = {
            'description':forms.Textarea(
                attrs={
                    'style':'width:100%;border-radius:3px;'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'style':'width:100%;border-radius:3px;'
                }
            )
        }
    def save(self, commit = True):
        recruiter = super().save(commit=False)
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if len(user)>0:
            raise UserAlreadyExists()
        else:
            new_user = User.objects.create(username=username)
            new_user.set_password(self.cleaned_data.get('password'))
            new_user.save()
            recruiter.user = new_user
        if commit:
            recruiter.save()
        return recruiter
        
class RecruiterLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'style': 'width:100%;border-radius:3px;'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'style': 'width:100%;border-radius:3px;'})
    )
    
class CreateJobForm(forms.ModelForm):
    techstack = forms.ModelMultipleChoiceField(
        queryset=TechStacks.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs={'style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;'})
    )
    profession_type = forms.ChoiceField(
        choices=PROFESSION_TYPE, 
        widget=forms.Select(attrs={'class': 'form-control','style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;'})
    )
    class Meta:
        model = Professions
        fields = ['name','description','location','md_content','profession_type','salary','experience']
        widgets = {
            'name': forms.TextInput(attrs={'style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;'}),
            'description': forms.TextInput(attrs={'style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;'}),
            'location': forms.TextInput(attrs={'style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;'}),
            'md_content': forms.FileInput(attrs={'style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;padding:5px'}),
            'salary': forms.NumberInput(attrs={'style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;padding:5px'}),
            'experience': forms.NumberInput(attrs={'style':'width: 100%;border: 1px solid #ccc; border-radius: 8px;outline: none; transition: box-shadow 0.2s ease-in-out;padding:5px'}),
        }
    def save(self,user,commit=True):
        profession = super().save(commit=False)
        profession.created_by = Recruiter.objects.get(user=user)
        if commit:
            profession.save()
        return profession