from django.urls import path
from .import views


urlpatterns = [
    path("", views.home, name="index"),
    path("profile/", views.profile, name="profile"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]