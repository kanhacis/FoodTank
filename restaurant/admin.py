from django.contrib import admin
from .models import Restaurant, Cuisine


# Register Restaurant model
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']

# Register Cuisine model
@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'cuisine']