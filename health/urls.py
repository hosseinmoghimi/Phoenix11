from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
 
    path('add-drug',login_required(apis.AddDrugApi.as_view()),name="add_drug"),
    path('drugs/',login_required(views.DrugsView.as_view()),name="drugs"),
    path('drug/<int:pk>/',login_required(views.DrugView.as_view()),name="drug"),  
 
    path('add-doctor',login_required(apis.AddDoctorApi.as_view()),name="add_doctor"),
    path('doctors/',login_required(views.DoctorsView.as_view()),name="doctors"),
    path('doctor/<int:pk>/',login_required(views.DoctorView.as_view()),name="doctor"),  
 
    path('add-patient',login_required(apis.AddPatientApi.as_view()),name="add_patient"),
    path('patients/',login_required(views.PatientsView.as_view()),name="patients"),
    path('patient/<int:pk>/',login_required(views.PatientView.as_view()),name="patient"),  
 
    path('add-prescription',login_required(apis.AddPrescriptionApi.as_view()),name="add_prescription"),
    path('prescriptions/',login_required(views.PrescriptionsView.as_view()),name="prescriptions"),
    path('prescription/<int:pk>/',login_required(views.PrescriptionView.as_view()),name="prescription"),  
    
]
