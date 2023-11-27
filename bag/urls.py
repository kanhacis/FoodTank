from django.urls import path
from .import views

# These bellow path's are rendering bag app's view.
urlpatterns = [
    path("add-to-bag/<int:id>", views.addToBag, name="add-to-bag"),
    path("view_bag/", views.viewBag, name="view_bag"),
    path("deleteItem/<int:id>", views.deleteItem, name="deleteItem"),
]