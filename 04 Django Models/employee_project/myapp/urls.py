from django.urls import path
from .views import employeeview

urlpatterns = [
    path('employees/', employeeview, name='employees'),
]
