from django.db import models
from user.models import User


VEG_OR_NONVEG_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
        ('Both', 'Both')
    ]
# Restaurant model
class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                    limit_choices_to={'user_type': 'Foodprovider'})  # ForeignKey to User
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    veg_or_nonveg = models.CharField(max_length=255, choices=VEG_OR_NONVEG_CHOICES)
    no_of_chefs = models.PositiveIntegerField()
    start_date = models.DateField()
    
    img1 = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    img2 = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    img3 = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    img4 = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # ForeignKey to Restaurant
    cuisine = models.CharField(max_length=255)

    def __str__(self):
        return self.cuisine
