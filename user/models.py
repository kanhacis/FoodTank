from django.db import models
from django.contrib.auth.models import AbstractUser


USER_TYPE = (
    ('Customer', 'Customer'),
    ('Foodprovider', 'Foodprovider'),
    ('Driver', 'Driver')
)
# Abstract User Model
class User(AbstractUser):
    mobile = models.CharField(max_length=255, unique=True)
    user_type = models.CharField(max_length=255, choices=USER_TYPE)

# Address Model
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, choices=[('Home', 'Home'), ('Work', 'Work')])

    def __str__(self):
        return self.city
    
# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()