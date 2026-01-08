from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home),
    path("about/", views.about),
    path("test_exception/", views.test_exception_view),
]
