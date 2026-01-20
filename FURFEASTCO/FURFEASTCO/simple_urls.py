"""
Simple URL configuration for testing
"""
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <h1 style="color: green;">✅ FURFEASTCO is running on Cloud Run!</h1>
    <p>This is a test page without database.</p>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/health/">Health Check</a></li>
        <li><a href="/test/">Test Page</a></li>
    </ul>
    """)

def health_check(request):
    return HttpResponse("OK", status=200)

def test_view(request):
    return HttpResponse("Test page is working!", status=200)

urlpatterns = [
    path('', home, name='home'),
    path('health/', health_check, name='health_check'),
    path('test/', test_view, name='test'),
]