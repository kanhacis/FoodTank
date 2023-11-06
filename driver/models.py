from django.db import models
from user.models import User


# Driver model
class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                limit_choices_to={'user_type': 'Driver'})  # ForeignKey to User
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Driver: {self.user.username}"