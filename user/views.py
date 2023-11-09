from django.shortcuts import render, redirect
from .models import User, Contact
from django.contrib import messages
from menu.models import Menu
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Define the home view function
def home(request):
    # Get all food data from Menu model
    menu = Menu.objects.all()

    # Prepare the context to pass data to the template
    context = {
        'menus': menu  # 'menus' key will be accessible in the template as a variable
    }

    # Render the 'home.html' template with the provided context
    return render(request, 'home.html', context)

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
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        user_type = request.POST['utype']
        password1 = request.POST['pwd']
        password2 = request.POST['pwdc']

        if password1 == password2:
            new_user = User.objects.create(username=name, email=email, mobile=mobile, user_type=user_type)
            new_user.set_password(password1)
            new_user.save()
            return redirect('/login/')
        else:
            message = messages.error(request, 'Password and confirm password is not match.')

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
                return redirect('/foods/')
                
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