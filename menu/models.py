from django.db import models
from user.models import User
from restaurant.models import Restaurant
from django.core.validators import MaxValueValidator, MinValueValidator


# Menu model
class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # ForeignKey to Restaurant
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(blank=True, default=True, null=True)
    cuisine = models.CharField(max_length=255, blank=True)
    img1 = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                    limit_choices_to={'user_type': 'Customer'})  # ForeignKey to User
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # ForeignKey to Menu
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    description = models.TextField()
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.menu.name}"