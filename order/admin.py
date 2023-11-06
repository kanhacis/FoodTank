from django.contrib import admin
from .models import Order, OrderItem


# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'restaurant', 'driver']

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'order', 'quantity']