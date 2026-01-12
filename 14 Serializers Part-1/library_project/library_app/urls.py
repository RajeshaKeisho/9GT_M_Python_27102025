from django.urls import path
from .views import author_list, author_detail, book_list, book_detail

urlpatterns = [
    path('authors/', author_list, name='author-list'),
    path('authors/<int:pk>/', author_detail, name='author-detail'),
    path('books/', book_list, name='book-list'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
]
