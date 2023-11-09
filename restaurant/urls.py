from django.urls import path
from .import views

urlpatterns = [
    path("restaurant/", views.restaurant, name="restaurant"),
    path("restaurant_info/<int:id>", views.restaurant_info, name="restaurant_info"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("addRestaurant/", views.addRestaurant, name="addRestaurant"),
    path("editRestaurant/<int:id>", views.editRestaurant, name="editRestaurant"), # working now
    path("deleteRestaurant/<int:id>", views.deleteRestaurant, name="deleteRestaurant"),

    path("addMenu/", views.addMenu, name="addMenu"),
    path("viewMenu/<int:id>", views.viewMenu, name="viewMenu"),
    path("editMenu/<int:id>", views.editMenu, name="editMenu"),
    path("deleteMenu/<int:id>", views.deleteMenu, name="deleteMenu"),
]