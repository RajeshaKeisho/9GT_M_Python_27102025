from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import UserGroup, UserProfile, Product

class Command(BaseCommand):
    help = 'Seed initial data for testing rate limiting'

    def handle(self, *args, **kwargs):
        # Create user groups
        free_group, _ = UserGroup.objects.get_or_create(
            name='Free Users',
            description='Free tier users',
            rate_limit_tier='free'
        )
        
        basic_group, _ = UserGroup.objects.get_or_create(
            name='Basic Users',
            description='Basic tier users',
            rate_limit_tier='basic'
        )
        
        premium_group, _ = UserGroup.objects.get_or_create(
            name='Premium Users',
            description='Premium tier users',
            rate_limit_tier='premium'
        )
        
        # Create users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass123'
            )
            
            # Assign to different groups
            if i == 0:
                group = free_group
            elif i in [1, 2]:
                group = basic_group
            else:
                group = premium_group
            
            UserProfile.objects.create(
                user=user,
                group=group,
                bio=f'Test user {i} bio'
            )
            users.append(user)
        
        # Create products
        products = [
            ('Laptop', 'High-performance laptop', 999.99),
            ('Phone', 'Smartphone with great camera', 699.99),
            ('Tablet', 'Portable tablet device', 399.99),
            ('Headphones', 'Noise-cancelling headphones', 199.99),
            ('Monitor', '4K Ultra HD monitor', 499.99),
        ]
        
        for name, description, price in products:
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                in_stock=True,
                created_by=users[0]  # First user creates all products
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded data!'))