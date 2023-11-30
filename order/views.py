from django.shortcuts import render, redirect
from bag.models import Bag, BagItem
from .models import Order, OrderItem


# Place order
def placeOrder(request):
    # Get the payment method type from the user
    paymentMethod = ''
    if request.method == 'POST':
        payment = request.POST.get('payment', '')
        paymentMethod += payment

    userBag = Bag.objects.get(user=request.user)
    bagItems = BagItem.objects.filter(bag=userBag)
    sum = 0 
    count = 0 

    for i in bagItems: 
        qunt = int(i.quantity)
        price = int(i.item.price)
        sum += qunt * price
        count += 1

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

    # user = request.user
    # restaurant = bagItems.first().item.restaurant
    # is_confirmed ?
    # estimated_time
    # driver
    # total_bill
    # transaction_id
    # payment_method
    # order_date = today auto save

    return redirect('/bag/view_bag/')