from django.shortcuts import render, redirect
from menu.models import Menu
from .models import Bag, BagItem


# Rendering add to bag page & write logic to add food in my bag.
def addToBag(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type=="Customer":
        return redirect("/login/")

    # Get the menu item
    menu_item = Menu.objects.get(id=id)

    # Check if the user has a bag
    user_bag, created = Bag.objects.get_or_create(user=request.user)

    # Check if the item is already in the bag
    bag_item, created = BagItem.objects.get_or_create(bag=user_bag, item=menu_item)
    if not created:
        bag_item.quantity += 1
        bag_item.save()

    return redirect('/foodprovider/restaurant_info/{}'.format(menu_item.restaurant.id)) 

# Rendering view bag page where user can see their food bag.
def viewBag(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type=="Customer":
        return redirect("/login/")
    
    user_bag = Bag.objects.get(user=request.user)
    bag_items = BagItem.objects.filter(bag=user_bag)

    sum = 0 
    count = 0 
    

    if request.method == "POST":
        for data in bag_items:
            data.quantity = request.POST.get(f"{data.id}")
            data.save()

    for i in bag_items: 
        qunt = int(i.quantity)
        price = int(i.item.price)
        sum += qunt * price
        count += 1
        
    context = { 
        'bag' : user_bag, 
        'bag_items' : bag_items, 
        'total' : sum, 
        'count' : count
    } 
    return render(request, "bag/basket.html", context) 

# Write logic to deleting an foodItem which exist in my bag.
def deleteItem(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type=="Customer":
        return redirect("/login/")
    
    bag_item = BagItem.objects.get(id=id)
    bag_item.delete()
    return redirect('/bag/view_bag/')