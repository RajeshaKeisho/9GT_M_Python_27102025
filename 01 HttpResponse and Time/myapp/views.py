from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
import pytz
# Create your views here.

def display(request):
    s = "<h1> Hello, Students, Welcome to Django Class! </h1>"
    return HttpResponse(s)

def my_view(request):
    return HttpResponse("Hello, world!")

def greeting(request):
    current_time = timezone.now()
    hour = current_time.hour
    if 6 <= hour <= 12:
        greeting_message = "Good Morning!"
    elif 12 <= hour <= 16:
        greeting_message = "Good Afternoon!"
    elif 16 <= hour <= 21:
        greeting_message = "Good Evening!"
    else:
        greeting_message = "Good Night!"
    formatted_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
    return HttpResponse(f"{greeting_message}! Today, the date and time is: {formatted_time} ")


def message(request):

    current_time_utc = timezone.now()

    ist_tz = pytz.timezone('Asia/Kolkata')
    current_time_ist = current_time_utc.astimezone(ist_tz)

    hour = current_time_ist.hour

    if 6 <= hour < 12:
        greeting_msg = "Hello Student!"
    elif 12 <= hour < 16:
        greeting_msg = "Hello, Good Afternoon!"
    elif 16 <= hour < 21:
        greeting_msg = "Hello, Good Evening!"
    elif 21 <= hour < 23:
        greeting_msg = "Hello, Good Night!"
    else:
        greeting_msg = "Hello, How are you?"

    formatted_time = current_time_ist.strftime("%d-%m-%Y %H:%M:%S")

    return HttpResponse(f"{greeting_msg} Today, the date and time in India is: {formatted_time}")







