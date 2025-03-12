from django import forms
from .models import UserJobApplication,Candidates
from django.forms import Textarea,TextInput,DateInput,FileInput,PasswordInput
from django.contrib.auth.models import User
from .exceptions import *
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'style':'width:100%;border-radius:7px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'style':'width:100%;border-radius:7px;'}))
    
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = UserJobApplication
        fields = ['get_hired']
        widgets = {
            'get_hired':Textarea(
                attrs={
                    'class':'get-hired-section',
                    'style':'width:100%;border-radius:10px;margin:0px;color:black;resize: none;',
                    'placeholder':'Enter Text Here!!'
                }
            )
        }

class CandidateRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        empty_value='False',
        widget=forms.TextInput(
                attrs={
                    'style': 'width:100%;border-radius:3px;',
                    'placeholder':'Enter Username Here!!'
                }
            )
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                'style': 'width:100%;border-radius:3px;',
                'placeholder':'Enter Password Here!!'
            }
        )
    )
    class Meta:
        model = Candidates
        fields = ['name','profile_pic','experiences','dob','md_content','resume']
        widgets = {
            'name' : TextInput(
                attrs = {
                    'style':'width:100%',
                    'placeholder':'Enter Name Here!!'
                }
            ),
            'dob': DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'style': 'width:100%;border-radius:3px;',
                    'placeholder': 'Enter DOB Here!!'
                },
            ),
            'resume': FileInput(
                attrs={
                    'style':'width:100%;border: 1px solid black;border-radius:3px;margin:10px 10px 10px 0px;padding:10px 10px 10px 10px;'
                }
            ),
            'profile_pic': FileInput(
                attrs={
                    'style':'width:100%;border: 1px solid black;border-radius:3px;margin:10px 10px 10px 0px;padding:10px 10px 10px 10px;'
                }
            ),
            'md_content': FileInput(
                attrs={
                    'style':'width:100%;border: 1px solid black;border-radius:3px;margin:10px 10px 10px 0px;padding:10px 10px 10px 10px;'
                }
            ),
            'experiences': Textarea(
                attrs={
                    'style':'width:100%;border: 1px solid black;border-radius:3px;margin:10px 10px 10px 0px;padding:10px 10px 10px 10px;'
                }
            )
        }
    def save(self, commit=True):
        candidate = super().save(commit=False)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username)
        if user is None or len(user)>0:
            raise UserAlreadyExistsException('User Already Exists!!')
        else:
            user = User.objects.create(username=username)
            user.set_password(password) 
            candidate.user = user
            user.save()
        if commit:
            candidate.save()
        return candidate
            