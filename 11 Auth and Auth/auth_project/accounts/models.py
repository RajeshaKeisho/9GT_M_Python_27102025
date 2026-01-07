import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    is_verified = models.BooleanField(default=False)  # New field for email verification
    email_verification_token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.username
