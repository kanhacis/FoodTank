from django.shortcuts import render, redirect
from .models import Restaurant
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import User


# Function (foodprovider dashboard)
# @login_required('/login/') # AttributeError: 'function' object has no attribute 'user'
def dashboard(request):
    # Check if the user is authenticated, if not, redirect them to the owner login page
    if not request.user.is_authenticated:
        return redirect("ownerlogin")
    
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
# @login_required('/login/')
def addRestaurant(request):
    if request.method == 'POST':
        # Get the restaurant data from the add_restaurant.html template
        uname = request.POST['uname']
        rname = request.POST['rname']
        rcity = request.POST['rcity']
        raddress = request.POST['raddress']
        rmobile = request.POST['rmobile']
        veg = request.POST['veg']
        nchefs = request.POST['nchefs']
        # rdate = request.POST['rdate']
        rimg1 = request.FILES.get('rimg1')
        rimg2 = request.FILES.get('rimg2')
        rimg3 = request.FILES.get('rimg3')
        rimg4 = request.FILES.get('rimg4')
        desc = request.POST['desc']

        user_obj = User.objects.get(username=uname)

        restaurant = Restaurant.objects.create(user=user_obj, name=rname, city=rcity, 
                                address=raddress, mobile=rmobile, veg_or_nonveg=veg, no_of_chefs=nchefs,
                                img1=rimg1, img2=rimg2, img3=rimg3, img4=rimg4, desc=desc)
        restaurant.save()
        message = messages.success(request, 'Restaurant created successfully!')

    return render(request, 'foodprovider/add_restaurant.html')

# Function to get all restaurant data
def restaurant(request):
    # get all restaurant data
    rst = Restaurant.objects.all()

    context = {
        'restaurants':rst,
    }
    return render(request, 'foodprovider/restaurant.html', context) 