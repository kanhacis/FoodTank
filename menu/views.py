from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from restaurant.models import Restaurant
from .models import Menu


# Rendering add menu page & write logic to create new menu.
def addMenu(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    rest_user = User.objects.get(username=request.user)
    restaurant_name = Restaurant.objects.filter(user=rest_user)

    if request.method == 'POST':
        rname = request.POST.get('rname')
        mname = request.POST.get('mname')
        mtype = request.POST.get('mtype')
        mcuisine = request.POST.get('mcuisine')
        mprice = request.POST.get('mprice')
        mimg1 = request.FILES.get('mimg1')
        mdesc = request.POST.get('mdesc')

        # Here could be many restaurant for a single admin.
        for i in restaurant_name:
            if i.name == rname:
                menu = Menu.objects.create(restaurant=i, name=mname, 
                                        type=mtype, price=mprice, cuisine=mcuisine, img1=mimg1, description=mdesc)
                menu.save()
                message = messages.success(request, 'Menu added successfully!')
                break

    context = {
        'restaurant_name' : restaurant_name
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
        mdesc = request.POST.get('mdesc')

        menuItem.name = mname
        menuItem.type = mtype
        menuItem.price = mprice
        menuItem.cuisine = mcuisine
        menuItem.img1 = mimg1
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