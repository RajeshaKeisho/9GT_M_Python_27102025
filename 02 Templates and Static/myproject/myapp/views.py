from django.shortcuts import render
import datetime
# Create your views here.
def wish1(request):
    time = datetime.datetime.now()
    name = "ABC"
    rollno = 101
    marks = 90
    formatted_time = time.strftime("%d-%m-%Y %H:%M:%S")

    my_dict = {
        'insert_date':formatted_time, 'name':name, 'rollno':rollno, 'marks':marks
    }

    return render(request, 'wish.html', my_dict)


def greet(request):
    now = datetime.datetime.now()
    current_time = now.strftime("%H %M %S")

    if now.hour < 12:
        greeting = "Good morning!"
    elif now.hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    return render(request, 'myapp/greet.html', {'greeting':greeting, 'current_time':current_time})
