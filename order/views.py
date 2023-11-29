from django.shortcuts import render, redirect
from bag.models import Bag, BagItem


# Place order
def placeOrder(request):
    # Get the payment method type from the user
    paymentMethod = ''
    if request.method == 'POST':
        payment = request.POST.get('payment', '')
        paymentMethod += payment

    # Retrieve the current user's bag items
    bagItems = BagItem.objects.filter(bag__user=request.user)

    # Assuming the bag has items
    # if bagItems.exists():
    #     # Assuming the bag items are associated with the same restaurant
    #     restaurant = bagItems.first().item.restaurant

    # id
    # user = request.user
    # restaurant = bagItems.first().item.restaurant
    # is_confirmed ?
    # estimated_time
    # driver
    # transaction_id
    # payment_method
    # order_date = today auto save

    return redirect('/bag/view_bag/')