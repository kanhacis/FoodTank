from django.urls import path
from .import views


# These bellow path's are rendering restaurant app's view.
urlpatterns = [
    path("adminSignup/", views.adminSignup, name="adminSignup"),
    path("adminSignin/", views.adminSignin, name="adminSignin"),

    path("restaurant/", views.restaurant, name="restaurant"),
    path("restaurant_info/<int:id>", views.restaurantInfo, name="restaurant_info"),

    path("dashboard/", views.adminDashboard, name="dashboard"),
    path("deleteTask/<int:id>", views.deleteTask, name="deleteTask"),
    path("addRestaurant/", views.addRestaurant, name="addRestaurant"),
    path("editRestaurant/<int:id>", views.editRestaurant, name="editRestaurant"), 
    path("deleteRestaurant/<int:id>", views.deleteRestaurant, name="deleteRestaurant"),
    path("restaurantOrder/<int:id>", views.restaurantOrder, name="restaurantOrder"),
    path("confirmOrder/<int:id>", views.confirmOrder, name="confirmOrder"),
]