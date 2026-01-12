from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
     class Meta:
          model = Author
          fields = "__all__"

class BookSerializer(serializers.Serializer):
     id = serializers.IntegerField(read_only=True)
     title = serializers.CharField(max_length=200)
     author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
     published_date = serializers.DateField()
     isbn = serializers.CharField(max_length=13)

     def create(self, validated_data):
          return Book.objects.create(**validated_data)
     
     def update(self, instance, validated_data):
          instance.title = validated_data.get("title", instance.title)
          instance.author = validated_data.get("author", instance.author)
          instance.published_date = validated_data.get("published_date", instance.published_date)
          instance.isbn = validated_data.get("isbn", instance.isbn)

          instance.save()
          return instance