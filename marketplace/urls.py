from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf.urls import handler500


def custom_500(request):
    return render(request, '500.html', status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('candidates.urls')),
    path('recruiter/',include('recruiters.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path("__reload__/", include("django_browser_reload.urls"))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler500 = 'marketplace.urls.custom_500'