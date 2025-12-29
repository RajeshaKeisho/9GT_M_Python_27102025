from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    published_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title