from django.db import models
from menu.models import Menu
from user.models import User

# Bag model
class Bag(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# BagItem model
class BagItem(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()