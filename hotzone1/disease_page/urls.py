from django.urls import path
from disease_page import views

urlpatterns = [
    path('all/<int:offset>', views.diseaseAllView.as_view(), name='disease_page'),
    path('all/', views.redirectView),
    path('all/query/<int:offset>', views.diseaseSearch, name='disease_search'),
    path('add/submit/', views.getNewDisease),
    path('add/', views.diseaseNewView, name='disease_add'),
    path('details/edit/submit/<int:pk>', views.getEditDisease, name='disease_edit_submit'),
    path('details/edit/submit/', views.redirectView),
    path('details/edit/delete/<int:pk>', views.deleteDisease, name='disease_delete'),
    path('details/edit/delete/', views.redirectView),
    path('details/edit/<int:pk>', views.diseaseEditView, name='disease_edit'),
    path('details/edit/', views.redirectView),
    path('details/<int:pk>', views.diseaseDetailsView.as_view(), name='disease_details'),
    path('details/', views.redirectView),
]
