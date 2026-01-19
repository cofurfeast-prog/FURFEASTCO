from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse('FURFEASTCO is running on Cloud Run!')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]
