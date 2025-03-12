from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Candidates)
admin.site.register(BookmarkedJobs)
admin.site.register(UserJobApplication)
admin.site.register(WorkExperience)