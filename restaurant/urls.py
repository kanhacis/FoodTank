from django.urls import path
from .import views

urlpatterns = [
    path("adminSignup/", views.adminSignup, name="adminSignup"),
    path("adminSignin/", views.adminSignin, name="adminSignin"),

    path("restaurant/", views.restaurant, name="restaurant"),
    path("restaurant_info/<int:id>", views.restaurant_info, name="restaurant_info"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("addRestaurant/", views.addRestaurant, name="addRestaurant"),
    path("editRestaurant/<int:id>", views.editRestaurant, name="editRestaurant"), # working now
    path("deleteRestaurant/<int:id>", views.deleteRestaurant, name="deleteRestaurant"),
]