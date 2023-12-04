from django.shortcuts import render, redirect
from menu.models import Menu
from .models import Bag, BagItem
from user.models import User, Address
from django.http import JsonResponse


# Rendering add to bag page & write logic to add food in my bag.
def addToBag(request, id):
    # Check if the user is authenticated, if not, return a JSON response indicating the need for login
    if not request.user.is_authenticated or not request.user.user_type == "Customer":
        return JsonResponse({'error': 'Authentication required'})

    # Get the menu item
    menuItem = Menu.objects.get(id=id)

    # Check if the user has a bag
    userBag, created = Bag.objects.get_or_create(user=request.user)

    # Check if the item is already in the bag
    bagItem, created = BagItem.objects.get_or_create(bag=userBag, item=menuItem)

    if not created:
        bagItem.quantity += 1
        bagItem.save()

    # Return a JSON response indicating success
    return JsonResponse({'status':'itemAdded'})

# Rendering view bag page where user can see their food bag.
def viewBag(request):
    if not request.user.is_authenticated or not request.user.user_type == "Customer":
        return redirect("/login/")
    
    address = Address.objects.filter(user=request.user)

    userBag = Bag.objects.get(user=request.user)
    bagItems = BagItem.objects.filter(bag=userBag)

    if request.method == "GET" and 'id' in request.GET:
        item_id = request.GET.get('id')
        foodId = item_id
        try:
            bag_item = BagItem.objects.get(id=item_id)
            new_quantity = int(request.GET.get('quantity', 0))

            if new_quantity >= 1:
                bag_item.quantity = new_quantity
                bag_item.save()
                price = bag_item.item.price * bag_item.quantity
                return JsonResponse({'status': 'Increase', 'price':price})
        except BagItem.DoesNotExist:
            pass    

    total = 0
    count = 0 
    for item in bagItems: 
        item_quantity = int(item.quantity)
        item_price = int(item.item.price)
        total += item_quantity * item_price
        count += 1
        
    context = { 
        'address': address,
        'bagItems': bagItems, 
        'total': total, 
        'count': count,
    } 
        
    return render(request, "bag/basket.html", context) 

# Write logic to deleting an foodItem which exist in my bag.
def deleteItem(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type=="Customer":
        return redirect("/login/")
    
    bagItem = BagItem.objects.get(id=id)
    price = bagItem.item.price * bagItem.quantity

    # Calculating total price for current bag items
    userBag = Bag.objects.get(user=request.user)
    bagItems = BagItem.objects.filter(bag=userBag)
    
    totalPrice = 0

    for item in bagItems: 
        item_quantity = int(item.quantity)
        item_price = int(item.item.price)
        totalPrice += item_quantity * item_price

    finalPrice = totalPrice - price
    
    bagItem.delete()
    return JsonResponse({'status':'itemDeleted', 'finalPrice':finalPrice})