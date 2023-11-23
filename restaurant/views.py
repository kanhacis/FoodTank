from django.shortcuts import render, redirect
from .models import Restaurant, Notification
from django.contrib import messages
from user.models import User, Address
from menu.models import Menu
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Admin signup page
def adminSignup(request):
    return render(request, 'restaurant_admin/signup.html')


# Admin login page
def adminSignin(request):
    return render(request, 'restaurant_admin/signin.html')


# Admin dashboard
def dashboard(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/foodprovider/adminSignin/")
    
    # Get the restaurant admin user object based on the currently logged-in user
    restaurant_admin = User.objects.get(username=request.user)

    # Retrieve the restaurant data associated with the admin user
    restaurant_data = Restaurant.objects.filter(user=restaurant_admin)

    # Create a context dictionary with the restaurant data to pass to the template
    context = {
        'my_restaurant' : restaurant_data
    }

    # Render the restaurant dashboard template with the context data
    # return render(request, 'foodprovider/restaurant_dashboard.html', context)
    return render(request, 'restaurant_admin/index.html', context)


# View restaurant
def restaurant(request):
    try:
        city = Address.objects.get(user=request.user)
        if request.method == 'GET':
            restaurant_name = request.GET.get('search-restaurant')
            if restaurant_name:
                restaurant = Restaurant.objects.filter(name__icontains=restaurant_name, city=city.city)
            else:
                restaurant = Restaurant.objects.filter(city=city.city)
    except:
        restaurant = Restaurant.objects.all()

    p = Paginator(restaurant, 4)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)

    except PageNotAnInteger:
        page_obj = p.page(1)

    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'foodprovider/restaurant.html', context)


# Add restaurants
def addRestaurant(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/foodprovider/adminSignin/")
    
    if request.method == 'POST':
        # Get the restaurant data from the add_restaurant.html template
        uname = request.POST.get('uname')
        rname = request.POST.get('rname')
        rcity = request.POST.get('rcity')
        raddress = request.POST.get('raddress') 
        rmobile = request.POST.get('rmobile')
        rtype = request.POST.get('rtype') 
        nchefs = request.POST.get('nchefs') 
        rdate = request.POST.get('rdate') 
        rimg1 = request.FILES.get('rimg1')
        rimg2 = request.FILES.get('rimg2')
        rimg3 = request.FILES.get('rimg3')
        rimg4 = request.FILES.get('rimg4')
        desc = request.POST.get('desc')

        print(uname, rname, raddress, rimg1)

        user_obj = User.objects.get(username=uname)

        restaurant = Restaurant.objects.create(user=user_obj, name=rname, city=rcity, 
                                address=raddress, mobile=rmobile, veg_or_nonveg=rtype, no_of_chefs=nchefs,
                                start_date=rdate, img1=rimg1, img2=rimg2, img3=rimg3, img4=rimg4, desc=desc)
        restaurant.save()
        message = messages.success(request, 'Restaurant created successfully!')

    # return render(request, 'foodprovider/add_restaurant.html')
    return render(request, 'restaurant_admin/addRestaurant.html')


# Edit restaurant
def editRestaurant(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    restaurant = Restaurant.objects.get(id=id)

    if request.method == "POST":
        uname = request.POST.get('uname')
        rname = request.POST.get('rname','')
        rcity = request.POST.get('rcity')
        raddress = request.POST.get('raddress')
        rmobile = request.POST.get('rmobile')
        rtype = request.POST.get('rtype')
        nchefs = request.POST.get('nchefs')
        rdate = request.POST.get('rdate')
        rimg1 = request.FILES.get('postImg')
        rimg2 = request.FILES.get('rimg2')
        rimg3 = request.FILES.get('rimg3')
        rimg4 = request.FILES.get('rimg4')
        desc = request.POST.get('desc')

        restaurant.user = request.user
        restaurant.name = rname
        restaurant.city = rcity
        restaurant.address = raddress
        restaurant.mobile = rmobile
        restaurant.veg_or_nonveg = rtype
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
    # return render(request, 'foodprovider/edit_restaurant.html', context)
    return render(request, 'restaurant_admin/editRestaurant.html', context)


# Delete restaurant
def deleteRestaurant(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/")
    
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    return redirect('/foodprovider/dashboard/')  


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


# Code for notification
def admin_notifications(request):
    admin_notifications = Notification.objects.filter(receiver=request.user, is_read=False)
    return render(request, 'admin_notifications.html', {'notifications': admin_notifications})