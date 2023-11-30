from django.urls import path
from .import views


urlpatterns = [
    path("", views.home, name="index"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signUp, name="signup"),
    path("login/", views.signIn, name="login"),
    path("orders/", views.orders, name="orders"),
    path("logout/", views.logOut, name="logout"),
    path("contact/", views.contact, name="contact"),
]