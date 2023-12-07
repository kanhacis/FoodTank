from django.shortcuts import render, redirect
from bag.models import Bag, BagItem
from .models import Order, OrderItem
from django.http import JsonResponse


# Place order
def placeOrder(request):
    # Get the payment method type from the user
    paymentMethod = ''
    if request.method == 'POST':
        payment = request.POST.get('payment', '')
        paymentMethod += payment

    userBag = Bag.objects.get(user=request.user)
    bagItems = BagItem.objects.filter(bag=userBag)
    
    # Calculate the total bill
    sum = 0 
    for i in bagItems: 
        qunt = int(i.quantity)
        price = int(i.item.price)
        sum += qunt * price

    # Retrieve the current user's bag items
    bagItems = BagItem.objects.filter(bag__user=request.user)

    # Assuming the bag has items
    if bagItems.exists():
        # Assuming the bag items are associated with the same restaurant
        restaurant = bagItems.first().item.restaurant

        # Create an order associated with the restaurant
        order = Order.objects.create(
            user = request.user,
            restaurant = restaurant,
            total_bill = sum,
            payment_method = paymentMethod,
        )    

        # Create order items linked to the created order
        for bag_item in bagItems:
            OrderItem.objects.create(
                order=order,
                item=bag_item.item,
                quantity=bag_item.quantity
            ) 

        # Clear the user's bag after placing the order
        bagItems.delete()
        
        # Send success response
        return JsonResponse({"status": "success"})

    return redirect('/bag/view_bag/')