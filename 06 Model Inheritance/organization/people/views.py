from django.shortcuts import render
from django.views.generic import ListView
from .models import EmployeeProxy, CustomerProxy
# Create your views here.

class EmployeeProxyView(ListView):
    model = EmployeeProxy
    template_name = 'people/employee_list.html'
    context_object_name = 'employees'

class CustomerProxyView(ListView):
    model = CustomerProxy
    template_name = 'people/customer_list.html'
    context_object_name = 'customers'