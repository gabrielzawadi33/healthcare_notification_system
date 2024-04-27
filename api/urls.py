from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PatientsByDoctorView, signup_nurse, patient_list




urlpatterns = [
    path('', views.home, name='home'),
    path('signup_nurse/', views.signup_nurse, name='signup_nurse'),
    path('login_nurse/', views.login_nurse, name='login_nurse'),
    path('nurse_dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path('signup_doctor/', views.signup_doctor, name='signup_doctor'),
    path('login_doctor/', views.login_doctor, name='login_doctor'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/<int:doctor_id>/patients/', PatientsByDoctorView.as_view()), #displays on te doctors dashboard
    path('doctors/<int:doctor_id>/patient_list/', PatientsByDoctorView.doctor_patient_list, name='doctor_patient_list'), #2
    path('register_patient/', views.register_patient, name='register_patient'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('nurse_after_login/', views.nurse_after_login, name='nurse_after_login'),
    path('doctor_patient_list/', views.doctor_patient_list, name='doctor_patient_list'),  #1.
    path('doctor/<int:doctor_id>/appointment/<int:patient_id>/', views.appointment_page, name='appointment_page'),
    path('doctor_schedule/<int:doctor_id>/', views.doctor_schedule, name='doctor_schedule'),
    path('appointment_list/<int:doctor_id>/', views.appointment_list, name='appointment_list'),
    

]

