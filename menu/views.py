from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from restaurant.models import Restaurant
from .models import Menu, Review
from django.http import JsonResponse


# Rendering add menu page & write logic to create new menu.
def addMenu(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    restUser = User.objects.get(username=request.user)
    restaurantName = Restaurant.objects.filter(user=restUser)

    if request.method == 'POST':
        rname = request.POST.get('rname')
        mname = request.POST.get('mname')
        mtype = request.POST.get('mtype')
        mcuisine = request.POST.get('mcuisine')
        mprice = request.POST.get('mprice')
        mimg1 = request.FILES.get('mimg1')
        mdesc = request.POST.get('mdesc')

        # Here could be many restaurant for a single admin.
        for i in restaurantName:
            if i.name == rname:
                menu = Menu.objects.create(restaurant=i, name=mname, 
                                        type=mtype, price=mprice, cuisine=mcuisine, img1=mimg1, description=mdesc)
                menu.save()
                message = messages.success(request, 'Menu added successfully!')
                break

    context = {
        'restaurantName' : restaurantName
    }
    return render(request, 'restaurant_admin/addMenu.html', context)

# Rendering view menu page.
def viewMenu(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    # Get restaurant name
    restaurant = Restaurant.objects.get(id=id)

    # Get all the menu's of restaurant
    allMenus = Menu.objects.filter(restaurant=restaurant)

    context = {
        "allMenus" : allMenus
    }

    # return render(request, 'foodprovider/view_menu.html', context)
    return render(request, 'restaurant_admin/viewMenu.html', context)

# Rendering edit menu page & write logic to edit an existing foodItem.
def editMenu(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    menuItem = Menu.objects.get(id=id)
    
    # Checking our data comes via a post request.
    if request.method == 'POST':
        mname = request.POST.get('mname')
        mtype = request.POST.get('mtype')
        mprice = request.POST.get('mprice')
        mcuisine = request.POST.get('mcuisine')
        mimg1 = request.FILES.get('mimg1')
        status = request.POST.get('menuStatus')
        mdesc = request.POST.get('mdesc')

        if status:
            status = True
        else:
            status = False

        menuItem.name = mname
        menuItem.type = mtype
        menuItem.price = mprice
        menuItem.cuisine = mcuisine
        menuItem.img1 = mimg1
        menuItem.available = status
        menuItem.description = mdesc

        menuItem.save()
        message = messages.success(request, 'Menu updated successfully!')
    
    context = {
        'menuItems' : menuItem
    }
    # return render(request, 'foodprovider/edit_menu.html', context)
    return render(request, 'restaurant_admin/editMenu.html', context)

# Write logic to deleting an existing foodItem.
def deleteMenu(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
        
    # Get the restaurant id using the menu id.
    restId = Restaurant.objects.get(menu__id=id)

    # Get a single menu item from menu model.
    menuItem = Menu.objects.get(id=id)

    # Now delete the menu item.
    menuItem.delete()
    return redirect('/menu/viewMenu/{}'.format(restId.id))

# Rating a menu
def ratingMenu(request, id):
    if request.method == "POST":
        rating = request.POST.get("rating", -1)
        desc = request.POST.get("desc", "")

        menuInstance = Menu.objects.get(id=id)
        reviewData = Review.objects.create(user=request.user, menu=menuInstance, rating=rating, description=desc)
        reviewData.save()
        return JsonResponse({"status":"success"})