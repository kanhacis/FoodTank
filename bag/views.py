from django.shortcuts import render, redirect
from menu.models import Menu
from .models import Bag, BagItem
from user.models import User, Address
import sweetify
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
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type=="Customer":
        return redirect("/login/")
    
    # Get user address
    address = Address.objects.filter(user=request.user)

    # Get data from user bag
    userBag = Bag.objects.get(user=request.user)

    # Filter our data from the bag item
    bagItems = BagItem.objects.filter(bag=userBag)

    sum = 0 
    count = 0 
    
    if request.method == "POST":
        for data in bagItems:
            data.quantity = request.POST.get(f"{data.id}")
            data.save()

    for i in bagItems: 
        qunt = int(i.quantity)
        price = int(i.item.price)
        sum += qunt * price
        count += 1
        
    context = { 
        'address' : address,
        'bagItems' : bagItems, 
        'total' : sum, 
        'count' : count
    } 
    return render(request, "bag/basket.html", context) 

# Write logic to deleting an foodItem which exist in my bag.
def deleteItem(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type=="Customer":
        return redirect("/login/")
    
    bagItem = BagItem.objects.get(id=id)
    bagItem.delete()
    return JsonResponse({'status':'itemDeleted'})

    # return redirect('/bag/view_bag/')
