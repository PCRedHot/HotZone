from django.urls import path
from login_page import views

urlpatterns = [
    path('', views.loginView, name='login_page'),
    path('attempt/', views.loginAttemptView, name='login_attempt'),
    path('logout/', views.logoutView, name='logout'),
]
