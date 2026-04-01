from django.urls import path
from .views import PatientIntakeView, PatientDetailView

urlpatterns = [
    path('patient-intake/', PatientIntakeView.as_view()),
    path('patients/<str:patient_id>/', PatientDetailView.as_view()),
]