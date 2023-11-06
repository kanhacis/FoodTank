from django.shortcuts import render
from .models import User
# from django.contrib.auth.models import User



# Home
def home(request):
    return render(request, 'home.html')

# Foods
def food(request):
    return render(request, 'foods.html')

# Contact
def contact(request):
    return render(request, 'contact.html')

# Signup
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

    return render(request, 'account/signup.html')

# Login
def login(request):
    return render(request, 'account/login.html')