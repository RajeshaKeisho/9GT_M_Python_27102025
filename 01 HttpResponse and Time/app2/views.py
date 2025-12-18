from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.

def morning_message(request):
    time = datetime.datetime.now()
    formatted_time = time.strftime('%d-%m-%Y %H:%M:%S')
    return HttpResponse("<h1> Hello, Good Morning Students, Welcome to Django Class! Now th etime is" + formatted_time + "</h1>")

def noon_message(request):
    time = datetime.datetime.now()
    formatted_time = time.strftime('%d-%m-%Y %H:%M:%S')
    return HttpResponse("<h1> Hello, Afternoon Students, Welcome to Django Class! Now th etime is" + formatted_time + "</h1>")

def evening_message(request):
    time = datetime.datetime.now()
    formatted_time = time.strftime('%d-%m-%Y %H:%M:%S')
    return HttpResponse("<h1> Hello, Good Evening Students, Welcome to Django Class! Now th etime is" + formatted_time + "</h1>")