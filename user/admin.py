from django.contrib import admin
from .models import User, Address, Contact

# Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'mobile', 'user_type']

# Register Address model
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'state', 'city', 'area']

# Register Contact model
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']