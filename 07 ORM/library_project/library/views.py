from django.shortcuts import render
from django.db.models import Q, F, Avg, Count, Max
from django.db import connection
from .models import Book, Author
# Create your views here.

def book_list(request):
    books = Book.objects.select_related("author").all()
    return render(request, "library/books.html", {"books": books})

def author_list(request):
    authors = Author.objects.all()
    return render(request, "library/authors.html", {"authors": authors})


def orm_queries(request):
    cheap_books = Book.objects.filter(price__lt=800)

    q_books = Book.objects.filter(
        Q(published_year__lt=2015) | Q(price__lt=300)
    )

    unavailable_books = Book.objects.exclude(available=True)

    increased_price = Book.objects.filter(price__lt=1000).update(
        price=F("price") + 50
    )

    avg_price = Book.objects.aggregate(avg=Avg("price"))
    max_price = Book.objects.aggregate(max=Max("price"))

    author_book_count = Author.objects.annotate(
        total_books=Count("book")
    )
    with connection.cursor() as cursor:
            cursor.execute("SELECT title, price FROM library_book WHERE price > 1000")
            raw_books = cursor.fetchall()

    context = {
        "cheap_books": cheap_books,
        "q_books": q_books,
        "unavailable_books": unavailable_books,
        "avg_price": avg_price,
        "max_price": max_price,
        "author_book_count": author_book_count,
        "raw_books": raw_books,
    }

    return render(request, "library/queries.html", context)

