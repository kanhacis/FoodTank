from django.urls import path
from .import views

urlpatterns = [
    path("addMenu/", views.addMenu, name="addMenu"),
    path("viewMenu/<int:id>", views.viewMenu, name="viewMenu"),
    path("editMenu/<int:id>", views.editMenu, name="editMenu"),
    path("deleteMenu/<int:id>", views.deleteMenu, name="deleteMenu"),
]