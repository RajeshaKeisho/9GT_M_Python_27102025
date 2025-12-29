from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="books"),
    path("authors/", views.author_list, name="authors"),
    path("queries/", views.orm_queries, name="queries"),
]