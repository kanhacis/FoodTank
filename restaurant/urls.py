from django.urls import path
from .import views

urlpatterns = [
    path("restaurant/", views.restaurant, name="restaurant"),
    path("addRestaurant/", views.addRestaurant, name="addRestaurant"),
    path("dashboard/", views.dashboard, name="dashboard"),
]