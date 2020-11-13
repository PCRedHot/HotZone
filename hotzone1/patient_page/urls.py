from django.urls import path
from patient_page import views

urlpatterns = [
    path('all/<int:offset>', views.patientAllView.as_view(), name='patient_page'),
    path('all/', views.redirectView),
    path('all/query/<int:offset>', views.patientSearch, name='patient_search'),
    path('add/submit/', views.getNewPatient),
    path('add/', views.patientNewView, name='patient_add'),
    path('details/edit/submit/<int:pk>', views.getEditPatient, name='patient_edit_submit'),
    path('details/edit/submit/', views.redirectView),
    path('details/edit/delete/<int:pk>', views.deletePatient, name='patient_delete'),
    path('details/edit/delete/', views.redirectView),
    path('details/edit/<int:pk>', views.patientEditView, name='patient_edit'),
    path('details/edit/', views.redirectView),
    path('details/<int:pk>', views.patientDetailsView.as_view(), name='patient_details'),
    path('details/', views.redirectView),
]
