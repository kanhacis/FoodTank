from django.db import models
from menu.models import Menu
from restaurant.models import Restaurant
from driver.models import Driver
from user.models import User, Address


payment_choices = (
    ('Cash on delivery', 'Cash on delivery'),
    ('Net banking', 'Net banking'),
    ('UPI', 'UPI'),
)


# Order model
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                        limit_choices_to={'user_type':'Customer'})
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    estimated_time = models.DateTimeField(blank=True, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    total_bill = models.IntegerField(blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True, choices=payment_choices)
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    deliveryAddress = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

# OrderItem model
class OrderItem(models.Model):
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.item.name