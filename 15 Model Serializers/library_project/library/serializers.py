from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)


    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'published_date', 'isbn']


    def valid_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 characters long.")
        return value
    
    def validate(self, data):
        if 'published_date' in data and data['published_date'] > timezone.now().date():
            raise serializers.ValidationError("Published date canno tbe i the future.")
        return data
