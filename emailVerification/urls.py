from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_attempt, name="Login"),
    path('logout', views.logout_attempt, name="Logout"),
    path('register/', views.register_attempt, name="Register"),
    path('email/confirmation/<str:activation_key>/', views.email_confirmation_attempt, name="ConfirmEmail"),
]
