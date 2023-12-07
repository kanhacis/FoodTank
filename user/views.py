from django.shortcuts import render, redirect
from .models import User, Contact, Address
from django.contrib import messages 
from restaurant.models import Restaurant
from menu.models import Menu, Review
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from django.db.models import Avg
import sweetify
from order.models import Order, OrderItem
from django.http import JsonResponse


# Rendering home page with all food items.
def home(request):
    try:
        if request.user.is_authenticated:
            # Retrieve the user's city based on their address
            userAddress = Address.objects.get(user=request.user)

            # Get all restaurants in the user's city
            userCityRestaurants = Restaurant.objects.filter(city=userAddress.city)
        else:
            # Show all menu items to anonymous users
            userCityRestaurants = Restaurant.objects.all()

        # Get the search term from the request (either food name or restaurant name)
        foodNameRestaurant = request.GET.get('search-food-restaurant')

        price = request.GET.get('price')
        url = ""
        restaurantUrl = ""

        # Build the base queryset
        foodRestaurant = Menu.objects.filter(restaurant__in=userCityRestaurants)

        # Apply filters based on user input
        if foodNameRestaurant:
            # Check if the search term corresponds to a restaurant
            restaurant = Restaurant.objects.filter(name__icontains=foodNameRestaurant).first()

            # If it's a restaurant, filter menus by that restaurant
            if restaurant:
                foodRestaurant = foodRestaurant.filter(restaurant=restaurant)
                restaurantUrl = restaurant
                restaurantUrl = restaurantUrl
                
            else:
                # If it's not a restaurant, assume it's a food item and filter menus by name
                foodRestaurant = foodRestaurant.filter(name__icontains=foodNameRestaurant)

        elif price:
            foodRestaurant = foodRestaurant.filter(price__lte=price)
            url = price

        # Add average rating to each menu item
        foodRestaurant = foodRestaurant.annotate(averageRating=Avg('review__rating'))

        # Prepare the context to pass data to the template
        context = {
            'foods': foodRestaurant,
            'url' : url,
            'restaurantUrl': restaurantUrl
        }

    except Address.DoesNotExist:
        # Handle the case where the user does not have an associated address
        context = {
            'foods': foodRestaurant,
            'url' : url,
            'restaurantUrl': restaurantUrl
        }

    return render(request, 'home.html', context)

# Rendering profile page.
def profile(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    user = request.user
    address, created = Address.objects.get_or_create(user=user)

    if request.method == "POST":
        print(request.POST.get('email', ''))

        user.first_name = request.POST.get('fname', '')
        user.last_name = request.POST.get('lname', '')
        user.email = request.POST.get('email', '')
        user.mobile = request.POST.get('mobile', '')

        address.state = request.POST.get('state', '')
        address.city = request.POST.get('city', '')
        address.area = request.POST.get('area', '')
        address.zipcode = request.POST.get('zipcode', '')
        address.house_no = request.POST.get('house', '1')
        address.category = request.POST.get('category', '')

        address.save()
        user.save()
        return JsonResponse({'status':'profileUpdate'})

    context = {
        'user_profile' : user,
        'user_address' : address
    }

    if request.user.user_type == "Customer":
        return render(request, 'account/profile.html', context)
    
    elif request.user.user_type == "Foodprovider":
        context['resturant_data'] = Restaurant.objects.filter(user=request.user)
        return render(request, 'restaurant_admin/profile.html', context)
    
    else:
        return render(request, 'account/profile.html', context)

# Rendering signup page & And registering user.
def signUp(request): 
    if request.method == 'POST': 
        name = request.POST.get('uname') 
        email = request.POST.get('email') 
        mobile = request.POST.get('mobile') 
        userType = request.POST.get('utype') 
        password1 = request.POST.get('pwd') 
        password2 = request.POST.get('pwdc') 

        print(name, email, mobile, userType, password1)


        if name and User.objects.filter(username=name).exists():
            return JsonResponse({'status':'userExist'})

        if email and User.objects.filter(email=email).exists():
            return JsonResponse({'status':'emailExist'})

        if mobile and User.objects.filter(mobile=mobile):
            return JsonResponse({'status':'mobileExist'})

        if password1 == password2:
            newUser = User.objects.create(username=name, email=email, mobile=mobile, user_type=userType)
            newUser.set_password(password1)
            newUser.save()

            if userType == "Customer":
                return JsonResponse({'status':'createAccount'})
            
            elif userType == "Foodprovider":
                return JsonResponse({'status':'createAccount'})

        else:
            # Error handling for password mismatch
            return JsonResponse({'status':'passwordNotMatch'})

    return render(request, 'account/signup.html')

# Rendering signin page & And authenticated user.
def signIn(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=uname, password=pwd)

        print("Admin", user)

        if user is not None:
            if user.user_type == "Customer":
                login(request, user)
                return JsonResponse({'status':'signIn'})
                
            elif user.user_type == "Foodprovider":
                login(request, user)
                return JsonResponse({'status':'signIn'})
                # return redirect('/foodprovider/dashboard/')
                
            elif user.user_type == "Driver":
                login(request, user)
                return redirect('/')  # Need to set the correct path
        else:
            return JsonResponse({'status':'invalidUser'})

    return render(request, 'account/login.html')

# Rendering orders page & showing my order history
@login_required(login_url='/login/')
def orders(request):
    # Only valid customer can access this page
    if not request.user.user_type == "Customer":
        return redirect("/login/")
    
    userOrders = Order.objects.filter(user=request.user)

    context = {
        'userOrders' : userOrders
    }

    return render(request, 'account/orders.html', context)

# Rendering orderInfo page & showing information of individual order.
def orderInfo(request, id):

    myOrders = OrderItem.objects.filter(order__order_id=id)
    
    context = {
        'myOrders' : myOrders
    }
    return render(request, 'account/orderInfo.html', context)

# Function to logout user 
@login_required(login_url='/login/') 
def logOut(request): 
    if request.user.user_type == "Customer":
        logout(request) 
        return redirect('/')
    elif request.user.user_type == "Foodprovider":
        logout(request)
        return redirect('/foodprovider/adminSignin/')
    else:
        logout(request) 
        return redirect('/')

# Contact page for everyone
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact.objects.create(name=name, email=email, subject=subject, message=message)
        contact.save()
        return JsonResponse({'status': 'Save'})
    
    return render(request, 'contact.html')
