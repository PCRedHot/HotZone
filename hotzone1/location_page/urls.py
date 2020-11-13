from django.urls import path
from location_page import views

urlpatterns = [
    path('all/<int:offset>', views.locationAllView.as_view(), name='location_page'),
    path('all/', views.redirectView),
    path('all/query/<int:offset>', views.locationSearch, name='location_search'),
    path('add/submit/', views.getNewLocation),
    path('add/', views.locationNewView, name='location_add'),
    path('details/edit/submit/<int:pk>', views.getEditLocation, name='location_edit_submit'),
    path('details/edit/submit/', views.redirectView),
    path('details/edit/delete/<int:pk>', views.deleteLocation, name='location_delete'),
    path('details/edit/delete/', views.redirectView),
    path('details/edit/query/<int:pk>', views.locationEditGeoDataView, name='location_edit_query'),
    path('details/edit/<int:pk>', views.locationEditView, name='location_edit'),
    path('details/edit/', views.redirectView),
    path('details/<int:pk>', views.locationDetailsView.as_view(), name='location_details'),
    path('details/', views.redirectView),
]
