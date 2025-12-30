from django.shortcuts import render, redirect
from .forms import JobApplicationForm, ContactForm
from django.contrib import messages
# Create your views here.

def job_application_view(request):
    form = JobApplicationForm()
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your application has been submitted succesfully!")
            return redirect("job_application")
    return render(request, 'applications/job_application.html', {'form':form})


def contact_view(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been succesfully!")
            return redirect("contact")
    return render(request, 'applications/contact.html', {'form':form})
            

