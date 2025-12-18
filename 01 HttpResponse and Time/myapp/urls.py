from django.urls import path
from .views import display, my_view, greeting, message


urlpatterns = [
    path('display/', display, name="display"),
    path('myview/', my_view, name="myview"),
    path('greeting/', greeting, name="greeting"),
    path('message/', message, name="message"),
]
