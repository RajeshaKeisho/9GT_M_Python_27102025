from django.shortcuts import render
from rest_framework import generics, pagination
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

class BookCursorPagination(pagination.CursorPagination):
    page_size = 10
    ordering = 'title'

class BookListViewPageNumber(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPageNumberPagination

class BookListViewLimitOffset(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookLimitOffsetPagination

class BookListViewCursor(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookCursorPagination


