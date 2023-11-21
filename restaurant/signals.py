from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from .models import Restaurant, Notification


@receiver(post_save, sender=Restaurant)
def notify_admin_on_restaurant_creation(sender, instance, **kwargs):
    if instance.user.user_type == 'Foodprovider':
        admin = User.objects.get(username='kanha') 
        message = f"New restaurant '{instance.name}' created by {instance.user.username}. Please verify."
        Notification.objects.create(sender=instance.user, receiver=admin, message=message) 
