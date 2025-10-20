from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from recruiters.models import Professions
from django.conf import settings
import os
from recruiters.models import TechStacks
from datetime import date
from cloudinary.models import CloudinaryField
# Create your models here.

class Candidates(models.Model):
    id = models.UUIDField(primary_key=True,auto_created=True,unique=True,editable=False,default=uuid4)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False,blank=False)
    name = models.CharField(null=False,blank=False,max_length=100)
    profile_pic = CloudinaryField('image',folder='profilepics')
    experiences = models.JSONField(null=True,blank=True)
    dob = models.DateField(blank=False,null=False,editable=True)
    created_on = models.DateField(default=date.today)
    md_content = CloudinaryField(resource_type='raw',folder='md_content')
    resume = CloudinaryField(resource_type='raw',folder='resume')
    def __str__(self):
        return self.user.username
    
class BookmarkedJobs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profession = models.ForeignKey(Professions,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} - {self.profession.name}'
    class Meta:
        unique_together = (('user','profession'),)
        
class UserJobApplication(models.Model):
    id = models.UUIDField(primary_key=True,auto_created=True,unique=True,editable=False,default=uuid4)
    profession = models.ForeignKey(Professions,on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidates,on_delete=models.CASCADE)
    get_hired = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.profession.name} - {self.candidate.user.username}'
    class Meta:
        unique_together = (('profession','candidate'),)
        
class WorkExperience(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    name = models.CharField(null=False,blank=False,max_length=100)
    description = models.TextField(blank=True,null=True,max_length=500)
    start_date = models.DateField(blank=False,null=False)
    end_date = models.DateField(blank=True,null=False)
    tech_stack = models.ManyToManyField(TechStacks,blank=True)