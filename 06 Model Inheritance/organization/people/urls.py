from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.EmployeeProxyView.as_view(), name='employee_list'),
    path('customers/', views.CustomerProxyView.as_view(), name='customer_list'),

]