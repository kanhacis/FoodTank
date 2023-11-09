from django.db import models
from menu.models import Menu
from restaurant.models import Restaurant
from driver.models import Driver
from user.models import User


# Order model
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                        limit_choices_to={'user_type':'Customer'})
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    estimated_time = models.DateTimeField()
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

# OrderItem model
class OrderItem(models.Model):
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()