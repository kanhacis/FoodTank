from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User
from restaurant.models import Restaurant
from .models import Menu


# Add Menu Function
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
        mprice = request.POST.get('mprice')
        mimg1 = request.FILES.get('mimg1')
        mdesc = request.POST.get('mdesc')

        for i in restaurant_name:
            print(i, " and ", rname)
            if i.name == rname:
                menu = Menu.objects.create(restaurant=i, name=mname, 
                                        type=mtype, price=mprice, img1=mimg1, description=mdesc)
                menu.save()
                message = messages.success(request, 'Menu added successfully!')
                break

    context = {
        'restaurant_name' : restaurant_name
    }
    return render(request, 'foodprovider/add_menu.html', context)

# View Menu
def viewMenu(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    # get restaurant name
    restaurant = Restaurant.objects.get(id=id)

    # get all the menu's of restaurant
    all_menus = Menu.objects.filter(restaurant=restaurant)

    context = {
        "all_menus" : all_menus
    }

    return render(request, 'foodprovider/view_menu.html', context)

# Edit Menu
def editMenu(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    menu_item = Menu.objects.get(id=id)
    
    if request.method == 'POST':
        mname = request.POST.get('mname')
        mtype = request.POST.get('mtype')
        mprice = request.POST.get('mprice')
        mimg1 = request.FILES.get('mimg1')
        mdesc = request.POST.get('mdesc')

        menu_item.name = mname
        menu_item.type = mtype
        menu_item.price = mprice
        menu_item.img1 = mimg1
        menu_item.description = mdesc

        menu_item.save()
        message = messages.success(request, 'Menu updated successfully!')
    
    context = {
        'menu_item' : menu_item
    }
    return render(request, 'foodprovider/edit_menu.html', context)

# Delete Menu
def deleteMenu(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    # get a single menu item
    menu_item = Menu.objects.get(id=id)
    menu_item.delete()
    return redirect('/foodprovider/viewMenu/')