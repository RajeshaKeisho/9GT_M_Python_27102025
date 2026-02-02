from django.db import models
from django.contrib.auth.models import User

class UserGroup(models.Model):
    """Custom user groups with rate limit tiers"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    rate_limit_tier = models.CharField(
        max_length=50,
        choices=[
            ('free', 'Free Tier'),
            ('basic', 'Basic Tier'),
            ('premium', 'Premium Tier'),
            ('enterprise', 'Enterprise Tier')
        ],
        default='free'
    )
    
    def __str__(self):
        return f"{self.name} ({self.rate_limit_tier})"

class UserProfile(models.Model):
    """Extended user profile with group membership"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Product(models.Model):
    """Example model for our API"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    
    class Meta:
        permissions = [
            ('can_view_premium_products', 'Can view premium products'),
        ]
    
    def __str__(self):
        return self.name

class Order(models.Model):
    """Another model for demonstration"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"
