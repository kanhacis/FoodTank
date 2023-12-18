from django.shortcuts import render, redirect
from .models import Restaurant, Notification, Todo
from django.contrib import messages
from user.models import User, Address
from menu.models import Menu
from order.models import Order, OrderItem
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from datetime import date
from django.db.models import Avg


# Rendering admin signup page.
def adminSignup(request):
    return render(request, 'restaurant_admin/signup.html')


# Rendering admin signin page.
def adminSignin(request):
    return render(request, 'restaurant_admin/signin.html')


# Rendering admin dashboard
def adminDashboard(request):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/foodprovider/adminSignin/")
    
    # Code for todo list start
    if request.method == 'POST':
        note = request.POST.get('note', '')
        data = Todo.objects.create(user=request.user, note=note)
        data.save()
        return JsonResponse({"status":"success"})
    # Code for todo list end
    
    # Get the restaurant admin user object based on the currently logged-in user
    restaurant_admin = User.objects.get(username=request.user)

    # Retrieve the restaurant data associated with the admin user
    restaurant_data = Restaurant.objects.filter(user=restaurant_admin)

    # Get all orders from the current user restaurant
    userRestaurant = Restaurant.objects.filter(user=request.user)
    myOrders = Order.objects.filter(restaurant__in=userRestaurant)

    # Calculating total amount
    totalOrder = 0
    totalAmount = 0
    for i in myOrders:
        if i.total_bill != None:
            if i.is_confirmed:
                totalOrder += 1
                totalAmount += i.total_bill

    # Calculating today amount
    todayAmount = 0
    todayOrder = 0
    today = date.today()
    for i in myOrders:
        if i.total_bill != None:
            if str(i.order_date)[0:10] == str(today):
                if i.is_confirmed:
                    todayAmount += i.total_bill
                    todayOrder += 1
    
    # Create a context dictionary with the restaurant data to pass to the template
    context = {
        'my_restaurant' : restaurant_data,
        'myOrders' : myOrders,
        'totalAmount' : totalAmount,
        'todayAmount' : todayAmount,
        'myTask' : Todo.objects.filter(user=request.user).order_by("-id"),
        'totalOrder': totalOrder,
        'todayOrder' : todayOrder
    }

    # Render the restaurant dashboard template with the context data
    # return render(request, 'foodprovider/restaurant_dashboard.html', context)
    return render(request, 'restaurant_admin/index.html', context)

# Delete today's task
def deleteTask(request, id):
    data = Todo.objects.get(id=id)
    data.delete()
    return JsonResponse({"status":"success"})

# Rendering restaurant page & showing all restaurants to users.
def restaurant(request):
    try:
        city = Address.objects.get(user=request.user, primary=True)
        if request.method == 'GET':
            restaurant_name = request.GET.get('search-restaurant')
            if restaurant_name:
                restaurant = Restaurant.objects.filter(name__icontains=restaurant_name, city=city.city).annotate(avg_rating=Avg('menu__review__rating')).order_by('-avg_rating')
            elif not city.city:
                restaurant = Restaurant.objects.all().annotate(avg_rating=Avg('menu__review__rating')).order_by('-avg_rating')
            else:
                restaurant = Restaurant.objects.filter(city=city.city).annotate(avg_rating=Avg('menu__review__rating')).order_by('-avg_rating')

                
    except:
        restaurant = Restaurant.objects.all().annotate(avg_rating=Avg('menu__review__rating')).order_by('-avg_rating')

    p = Paginator(restaurant, 10)
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


# Rendering add restaurant page & write logic to create new restaurant.
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

        user_obj = User.objects.get(username=uname)

        restaurant = Restaurant.objects.create(user=user_obj, name=rname, city=rcity, 
                                address=raddress, mobile=rmobile, veg_or_nonveg=rtype, no_of_chefs=nchefs,
                                start_date=rdate, img1=rimg1, img2=rimg2, img3=rimg3, img4=rimg4, desc=desc)
        restaurant.save()
        return JsonResponse({"status":"restaurantAdded"})
        

    # return render(request, 'foodprovider/add_restaurant.html')
    return render(request, 'restaurant_admin/addRestaurant.html')


# Rendering edit restaurant page & write logic to edit an existing restaurant.
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


# Write logic to delete an existing restaurant.
def deleteRestaurant(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated or not request.user.user_type == "Foodprovider":
        return redirect("/login/") 
    
    restaurant = Restaurant.objects.get(id=id) 
    restaurant.delete() 
    return redirect('/profile/') 


# Restaurant orders details
def restaurantOrder(request, id):
    orderInfo = OrderItem.objects.filter(order__order_id=id)

    order = Order.objects.get(order_id=id)
    deliveryAdd = order.deliveryAddress

    context = {
        "orderInfo": orderInfo,
        "deliveryAdd": deliveryAdd
    }
    return render(request, "restaurant_admin/restaurantOrder.html", context)
 
 
# Confirm order 
def confirmOrder(request, id): 
    order = Order.objects.get(order_id=id) 
    order.is_confirmed = True 
    # order.save() 

    dataList = [order.order_id, order.order_date, order.user.username, order.total_bill, order.is_confirmed]
    return JsonResponse({"status":"success", "dataList":dataList})

# Rendering restaurant information page & this shows the individual restaurant information to users.
def restaurantInfo(request, id):
    # Check if the user is authenticated, if not, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    try:
        if request.method == "GET":
            food = request.GET.get('search-food-cuisine')
            price = request.GET.get('price')
            ftype = request.GET.get('ftype')
           
            restId = Restaurant.objects.get(id=id)
            if food:
                restIdMenus = Menu.objects.filter(restaurant=restId, name__icontains=food)

                if not restIdMenus:
                    restIdMenus = Menu.objects.filter(restaurant=restId, cuisine__icontains=food)

            elif price:
                restIdMenus = Menu.objects.filter(restaurant=restId, price__lte=price)

            elif ftype:
                restIdMenus = Menu.objects.filter(restaurant=restId, type__icontains=ftype)

            else:
                restIdMenus = Menu.objects.filter(restaurant=restId)

            context = {
                'restId': restId,
                'restIdMenus': restIdMenus
            }

    except:
        restId = Restaurant.objects.get(id=id)
        restIdMenus = Menu.objects.filter(restaurant=restId)

    restaurant = Restaurant.objects.get(id=id)
    context = {
        'price' : price,
        'restId': restId,
        'restIdMenus': restIdMenus,
        'restaurant':restaurant
    }

    return render(request, 'foodprovider/restaurant_info.html', context)
 

# Notification functionality work is not done yet.
def adminNotifications(request):
    admin_notifications = Notification.objects.filter(receiver=request.user, is_read=False)
    return render(request, 'admin_notifications.html', {'notifications': admin_notifications})