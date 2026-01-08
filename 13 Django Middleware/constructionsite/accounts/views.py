from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, "home.html")

def about(request):
    return HttpResponse("<html><body><h1>About Us</h1><p>This is the about page.</p></body></html")


def test_exception_view(request):
    pass
    return HttpResponse("View Executed successfully if there is no execption middleware")