from django.urls import path
from case_page import views

urlpatterns = [
    path('disease/<int:pk>/<int:offset>', views.diseaseCaseView, name='case_disease'),
    path('disease/<int:pk>/add/submit/', views.getNewCase),
    path('disease/<int:pk>/add/', views.diseaseCaseAddView, name='case_disease_add'),
    path('disease/<int:pk>/query/<int:offset>', views.diseaseCaseSearchView, name='case_disease_search'),
    path('disease/all/<int:offset>', views.chooseDiseaseView, name='case_choose_disease'),
    path('disease/all/query/<int:offset>', views.chooseDiseaseSearchView, name='case_choose_disease_search'),
    path('location/details/add/query/submit/<int:pk>', views.getNewPlace),
    path('location/details/add/query/<int:pk>', views.locationAddSearchView, name='case_location_add_search'),
    path('location/details/add/submit/<int:pk>', views.getLocationAddView),
    path('location/details/add/<int:pk>', views.locationAddView, name='case_location_add'),
    path('location/details/delete/<int:pk>', views.locationDeleteView, name='case_location_delete'),
    path('location/details/edit/submit/<int:pk>', views.getLocationEditView),
    path('location/details/edit/<int:pk>', views.locationEditView, name='case_location_edit'),
    path('location/details/<int:pk>', views.locationDetailsView, name='case_location_details'),
    path('details/delete/<int:pk>', views.caseDeleteView, name='case_delete'),
    path('details/<int:pk>', views.caseDetailsView, name='case_details')
]
