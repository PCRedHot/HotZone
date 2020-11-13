from django.urls import path
from main_page import views

urlpatterns = [
    path('', views.mainView.as_view(), name='main_page')
]
