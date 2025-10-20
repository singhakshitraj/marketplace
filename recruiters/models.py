from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.conf import settings
import os
from datetime import datetime
from cloudinary.models import CloudinaryField
# Create your models here.
PROFESSION_TYPE = [
    ('JOBS','JOBS'),
    ('INTERNSHIP','INTERNSHIP'),
    ('FREELANCE','FREELANCE')
]
class Recruiter(models.Model):
    id = models.UUIDField(auto_created=True,primary_key=True,unique=True,editable=False,default=uuid4)
    user = models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)
    profile_pic = CloudinaryField('image',folder='profilepics')
    name = models.CharField(null=False,blank=False,max_length=100)
    description = models.TextField(null=False,blank=False)
    def __str__(self) -> str:
        return self.user.username

    
class TechStacks(models.Model):
    id = models.UUIDField(primary_key=True,auto_created=True,unique=True,editable=False,default=uuid4)
    name = models.CharField(null=False,blank=False,max_length=100)
    description = models.TextField(blank=False,null=False)
    def __str__(self) -> str:
        return self.name

class Professions(models.Model):
    id = models.UUIDField(primary_key=True,auto_created=True,unique=True,editable=False,default=uuid4)
    name = models.CharField(null=False,blank=False,max_length=100)
    description = models.CharField(max_length=500,null=False,blank=False)
    location = models.CharField(blank=False,null=False,max_length=100)
    md_content = CloudinaryField(resource_type='raw',folder='job_description')
    techstack = models.ManyToManyField(TechStacks,)
    profession_type = models.CharField(choices=PROFESSION_TYPE,max_length=100)
    salary = models.BigIntegerField()
    experience = models.IntegerField()
    created_by = models.ForeignKey(to=Recruiter,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name

    