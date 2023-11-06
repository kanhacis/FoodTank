from django.contrib import admin
from .models import Menu, Review


# Register Menu model
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'name', 'type', 'price']

# Register Review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu', 'rating']