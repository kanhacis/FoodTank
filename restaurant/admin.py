from django.contrib import admin
from .models import Restaurant, Cuisine, Notification, Todo


# Register Restaurant model
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'is_verified']

# Register Cuisine model
@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'cuisine']

# Register Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'message', 'timestamp', 'is_read']

# Register Todo model
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['done', 'note']