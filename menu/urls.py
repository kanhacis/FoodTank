from django.urls import path
from .import views


# These bellow path's are rendering menu app's view.
urlpatterns = [
    path("addMenu/", views.addMenu, name="addMenu"),
    path("viewMenu/<int:id>", views.viewMenu, name="viewMenu"),
    path("editMenu/<int:id>", views.editMenu, name="editMenu"),
    path("deleteMenu/<int:id>", views.deleteMenu, name="deleteMenu"),
    path("ratingMenu/<int:id>", views.ratingMenu, name="ratingMenu"),
]