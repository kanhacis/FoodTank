from django.shortcuts import render, redirect
from .models import Restaurant
from django.contrib import messages
from user.models import User
from menu.models import Menu
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Function (foodprovider dashboard)
def dashboard(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    # Get the restaurant admin user object based on the currently logged-in user
    restaurant_admin = User.objects.get(username=request.user)

    # Retrieve the restaurant data associated with the admin user
    restaurant_data = Restaurant.objects.filter(user=restaurant_admin)

    # Create a context dictionary with the restaurant data to pass to the template
    context = {
        'my_restaurant' : restaurant_data
    }

    # Render the restaurant dashboard template with the context data
    return render(request, 'foodprovider/restaurant_dashboard.html', context)

# Function (Add restaurants)
def addRestaurant(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    if request.method == 'POST':
        # Get the restaurant data from the add_restaurant.html template
        uname = request.POST.get('uname')
        rname = request.POST.get('rname','')
        rcity = request.POST.get('rcity')
        raddress = request.POST.get('raddress')
        rmobile = request.POST.get('rmobile')
        veg = request.POST.get('veg')
        nchefs = request.POST.get('nchefs')
        rdate = request.POST.get('rdate')
        rimg1 = request.FILES.get('rimg1')
        rimg2 = request.FILES.get('rimg2')
        rimg3 = request.FILES.get('rimg3')
        rimg4 = request.FILES.get('rimg4')
        desc = request.POST.get('desc')

        user_obj = User.objects.get(username=uname)

        restaurant = Restaurant.objects.create(user=user_obj, name=rname, city=rcity, 
                                address=raddress, mobile=rmobile, veg_or_nonveg=veg, no_of_chefs=nchefs,
                                start_date=rdate, img1=rimg1, img2=rimg2, img3=rimg3, img4=rimg4, desc=desc)
        restaurant.save()
        message = messages.success(request, 'Restaurant created successfully!')

    return render(request, 'foodprovider/add_restaurant.html')

# Edit restaurant
def editRestaurant(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    restaurant = Restaurant.objects.get(id=id)

    if request.method == "POST":
        uname = request.POST.get('uname')
        rname = request.POST.get('rname','')
        rcity = request.POST.get('rcity')
        raddress = request.POST.get('raddress')
        rmobile = request.POST.get('rmobile')
        veg = request.POST.get('veg')
        nchefs = request.POST.get('nchefs')
        rdate = request.POST.get('rdate')
        rimg1 = request.FILES.get('rimg1')
        rimg2 = request.FILES.get('rimg2')
        rimg3 = request.FILES.get('rimg3')
        rimg4 = request.FILES.get('rimg4')
        desc = request.POST.get('desc')

        restaurant.user = request.user
        restaurant.name = rname
        restaurant.city = rcity
        restaurant.address = raddress
        restaurant.mobile = rmobile
        restaurant.veg_or_nonveg = veg
        restaurant.no_of_chefs = nchefs
        restaurant.start_date = rdate
        restaurant.img1 = rimg1
        restaurant.img2 = rimg2
        restaurant.img3 = rimg3
        restaurant.img4 = rimg4
        restaurant.desc = desc

        restaurant.save()
        message = messages.success(request, 'Restaurant updated successfully!')

    context = {
        'restaurant' : restaurant
    }
    return render(request, 'foodprovider/edit_restaurant.html', context)

# Delete restaurant
def deleteRestaurant(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    return redirect('/foodprovider/dashboard/')

# Add Menu Function
def addMenu(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
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

# View Individual restaurants menu's
def viewMenu(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
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
    if not request.user.is_authenticated:
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
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    # get a single menu item
    menu_item = Menu.objects.get(id=id)
    menu_item.delete()
    return redirect('/foodprovider/viewMenu/')

# Function to get all restaurant data
def restaurant(request):
    # get all restaurant data
    rst = Restaurant.objects.all()
    p = Paginator(rst, 4)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'restaurants':rst,
        'page_obj': page_obj
    }
    return render(request, 'foodprovider/restaurant.html', context) 

# Individual Restaurant Information
def restaurant_info(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    rest_id = Restaurant.objects.get(id=id)
    rest_id_menus = Menu.objects.filter(restaurant=rest_id)
    context = {
        'rest_id' : rest_id,
        'rest_id_menus' : rest_id_menus
    }

    return render(request, 'foodprovider/restaurant_info.html', context) 
