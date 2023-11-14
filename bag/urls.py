from django.urls import path
from .import views


urlpatterns = [
    path("add-to-bag/<int:id>", views.add_to_bag, name="add-to-bag"),
    path("view_bag/", views.view_bag, name="view_bag"),
    path("deleteItem/<int:id>", views.deleteItem, name="deleteItem"),
]