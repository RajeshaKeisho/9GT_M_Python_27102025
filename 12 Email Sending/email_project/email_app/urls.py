from django.urls import path
from . import views

urlpatterns = [
    path('send_email/', views.send_email, name='send_email'),
    path('form/', views.form_view, name='form_view'),
]
