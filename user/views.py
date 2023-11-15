from django.shortcuts import render, redirect
from .models import User, Contact, Address
from django.contrib import messages 
from restaurant.models import Restaurant
from menu.models import Menu
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 


# Define the home view function
def home(request):
    city = Address.objects.get(user=request.user)
    rest = Restaurant.objects.filter(city=city.city)
    
    if request.method == 'GET':
        food_name_restaurant = request.GET.get('search-food-restaurant')
        if food_name_restaurant:
            # Check if the search term corresponds to a restaurant
            restaurant = Restaurant.objects.filter(name__icontains=food_name_restaurant).first()
            if restaurant:
                # If it's a restaurant, filter menus by that restaurant
                food_restaurant = Menu.objects.filter(restaurant=restaurant, restaurant__in=rest)
            else:
                # If it's not a restaurant, assume it's a food item and filter menus by name
                food_restaurant = Menu.objects.filter(name__icontains=food_name_restaurant, restaurant__in=rest)
        else:
            # If no search term provided, show all menus
            food_restaurant = Menu.objects.filter(restaurant__in=rest)

    # Pagination
    p = Paginator(food_restaurant, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    # Prepare the context to pass data to the template
    context = {
        'page_obj': page_obj
    }

    # Render the 'home.html' template with the provided context
    return render(request, 'home.html', context)

# Profile
def profile(request):
    user = request.user
    address, created = Address.objects.get_or_create(user=user)

    if request.method == "POST":
        state = request.POST.get('state')
        city = request.POST.get('city')
        area = request.POST.get('area')
        zipcode = request.POST.get('zipcode')
        category = request.POST.get('category')

        address.user = user
        address.state = state
        address.city = city
        address.area = area
        address.zipcode = zipcode
        address.category = category
        address.save()
        message = messages.success(request, "Your profile is completed.")
    
    context = {
        'user_profile' : user,
        'user_address' : address
    }
    return render(request, 'account/profile.html', context)

# Contact
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        sbj = request.POST['subject']
        msg = request.POST['message']

        contact = Contact.objects.create(name=name, email=email, subject=sbj, message=msg)
        contact.save()
        message = messages.success(request, 'Message sent successfully!')

            
    return render(request, 'contact.html')

# Function to signup user 
def signup(request): 
    if request.method == 'POST': 
        name = request.POST.get('name') 
        email = request.POST.get('email') 
        mobile = request.POST.get('mobile') 
        user_type = request.POST.get('utype') 
        password1 = request.POST.get('pwd') 
        password2 = request.POST.get('pwdc') 

        if User.objects.filter(username=name).exists():
            messages.error(request, "Account with this username is already exist.")
            return redirect('/signup/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Account with this email is already exist.")
            return redirect('/signup/')

        if User.objects.filter(mobile=mobile):
            messages.error(request, "Account with this mobile number is alread exist.")
            return redirect('/signup/')

        # Additional checks (e.g., password strength)
        if len(password1) < 4:
            messages.error(request, 'Password should be at least 8 characters long.')
            return render(request, 'account/signup.html')

        if password1 == password2:
            new_user = User.objects.create(username=name, email=email, mobile=mobile, user_type=user_type)
            new_user.set_password(password1)
            new_user.save()

            if user_type == "Customer":
                return redirect('/profile/')
            else:
                return redirect('/login/')

        else:
            # Error handling for password mismatch
            messages.error(request, 'Password and confirm password do not match.')
            return render(request, 'account/signup.html')

    return render(request, 'account/signup.html')

# Function to login user
def Login(request):
    if request.method == 'POST':
        uname = request.POST['name']
        pwd = request.POST['password']
        utype = request.POST['utype'] 

        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            if utype == "Customer" and user.user_type == "Customer":
                login(request, user)
                return redirect('/')
                
            elif utype == "Foodprovider" and user.user_type == "Foodprovider":
                login(request, user)
                return redirect('/foodprovider/dashboard/')
                
            elif utype == "Driver" and user.user_type == "Driver":
                login(request, user)
                return redirect('/')  # Need to set the correct path
                
            else:
                message = messages.error(request, 'You are not authorized to log in as a {}.'.format(utype))
        else:
            message = messages.error(request, 'Invalid username or password. Please try again.')


    return render(request, 'account/login.html')

# Function to logout user 
@login_required(login_url='/login/') 
def Logout(request): 
    logout(request) 
    return redirect('/')
