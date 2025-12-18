from django.urls import path
from .views import wish1, greet

urlpatterns = [
    path('wish/', wish1, name='wish'),
    path('greet/', greet, name='greet'),
]
