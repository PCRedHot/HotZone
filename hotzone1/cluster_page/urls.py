from django.urls import path
from cluster_page import views

urlpatterns = [
    path('disease/<int:disease>', views.clusterOptionView, name='cluster_option_page'),
    path('disease/view/<int:disease>', views.clusterView, name='cluster_view_page'),
]
