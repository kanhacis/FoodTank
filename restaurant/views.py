from django.shortcuts import render


# Function to get all restaurant data
def restaurant(request):
    return render(request, 'foodprovider/restaurant.html') 