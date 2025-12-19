from django.urls import path
from .views import home, category_news

urlpatterns = [
    path('', home, name='home'),
    path('category/<str:category>/', category_news, name='category_news'),
]
