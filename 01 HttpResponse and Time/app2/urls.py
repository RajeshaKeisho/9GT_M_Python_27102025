from django.urls import path
from .views import morning_message, noon_message, evening_message


urlpatterns = [
    path('morning/', morning_message, name="morning"),
    path('noon/', noon_message, name="noon"),
    path('evening/', evening_message, name="evening"),
]