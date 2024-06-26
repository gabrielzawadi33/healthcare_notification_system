import datetime
from django.utils import timezone
from venv import logger
from django.shortcuts import redirect, render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.task import check_appointments
from .models import Appointment, Doctor, Nurse, Patient
from .serializers import DoctorSerializers, NurseSerializers, PatientSerializer
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from channels.generic.websocket import AsyncWebsocketConsumer
import json


channel_layer = get_channel_layer()

def home(request):
    return render(request, 'healthcare/Home_page.html')

def nurse_dashboard(request):
    doctors = Doctor.objects.all()
    return render(request, 'healthcare/Nurse_After_login.html', {'doctors': doctors})

@api_view(['POST', 'GET'])
def login_nurse(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        logger.info(f'Attempting to authenticate user with email: {email}')
        if email and password:
            try:
                user = Nurse.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    logger.info(f'User {email} authenticated successfully')
                    return redirect('nurse_dashboard')
                else:
                    messages.error(request, 'Invalid username or password.')
                    logger.warning(f'Failed to authenticate user {email}: Invalid password')
            except Nurse.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                logger.warning(f'Failed to authenticate user {email}: User does not exist')
    return render(request, 'healthcare/login_nurse.html')

@api_view(['POST','GET'])
def signup_nurse(request):
    if request.method == 'POST':
        serializer = NurseSerializers(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return redirect('login_nurse')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return render(request, 'healthcare/signup_nurse.html')

@api_view(['POST','GET'])
def signup_doctor(request):
    if request.method == 'POST':
        serializer = DoctorSerializers(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return redirect('login_doctor')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return render(request, 'healthcare/signup_doctor.html')

@api_view(['POST','GET'])
def login_doctor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        logger.info(f'Attempting to authenticate user with email: {email}')
        if email and password:
            try:
                user = Doctor.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    logger.info(f'User {email} authenticated successfully')
                    return redirect('doctor_dashboard')
                else:
                    messages.error(request, 'Invalid username or password.')
                    logger.warning(f'Failed to authenticate user {email}: Invalid password')
            except Doctor.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                logger.warning(f'Failed to authenticate user {email}: User does not exist')
    return render(request, 'healthcare/login_doctor.html')




from django.db.models import F, ExpressionWrapper, DateTimeField
from datetime import timedelta
from .models import Patient, Appointment

def doctor_dashboard(request):
    doctor_id = request.session.get('user_id')
    patients = Patient.objects.filter(doctor_id=doctor_id)
    patient_count = patients.count()
    now = timezone.now()

    # Assuming the current timezone is the correct one
    tz = timezone.get_current_timezone()
    now_local = now.astimezone(tz) + timedelta(hours=3)

    today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_start = today_start + timedelta(days=1)

    # Get appointments for today, sorted by appointment_date, and subtract 3 hours from each appointment_date
    appointments_today = Appointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date__range=(now_local, tomorrow_start)
    ).annotate(
        adjusted_appointment_date=ExpressionWrapper(
            F('appointment_date') - timedelta(hours=3),
            output_field=DateTimeField()
        )
    ).order_by('appointment_date')

    # Convert adjusted_appointment_date to local timezone
    for appointment in appointments_today:
        appointment.adjusted_appointment_date = appointment.adjusted_appointment_date.astimezone(tz)
        print(f"Adjusted time for appointment: {appointment.adjusted_appointment_date.strftime('%H:%M')}")

    appointment_count = appointments_today.count()

    context = {
        'patients': patients,
        'patient_count': patient_count,
        'doctor_id': doctor_id,
        'appointment_count': appointment_count,
        'today': today_start,
        'appointments_today': appointments_today
    }
    return render(request, 'healthcare/Doctor_After_login.html', context)


class PatientsByDoctorView(APIView):
    def get(self, request, doctor_id, format=None):
        patients = Patient.objects.filter(doctor__id=doctor_id)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def doctor_patient_list(request, doctor_id):
        patients = Patient.objects.filter(doctor__id=doctor_id).exclude(appointment__doctor__id=doctor_id).order_by('-id')
        return render(request, 'healthcare/Doctor_patient_list.html', {'patients': patients})

def register_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        patient_id = request.POST.get('patient_id')
        address = request.POST.get('address')
        doctor_id = request.POST.get('doctor')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        roomNo = request.POST.get('roomNo')
        phone_number = request.POST.get('phone_number')
        health_insurance = request.POST.get('health_insurance')

        doctor = Doctor.objects.get(id=doctor_id)

        patient = Patient(
            name=name, 
            patient_id=patient_id, 
            address=address, 
            doctor=doctor, 
            date_of_birth=date_of_birth, 
            gender=gender, 
            phone_number=phone_number, 
            health_insurance=health_insurance
        )

        patient.save()

        messages.success(request, 'Patient registered successfully')
        return redirect('nurse_dashboard')

    else:
        doctors = Doctor.objects.all()
        return render(request, 'healthcare/Nurse_After_login.html', {'doctors': doctors})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'healthcare/Nurse_patients_list.html', {'patients': patients})


def nurse_after_login(request):
    doctors = Doctor.objects.all()
    return render(request, 'healthcare/Nurse_After_login.html', {'doctors': doctors})



def doctor_patient_list(request):
    # Retrieve the logged-in doctor's ID
    doctor_id = request.session.get('user_id')
    # Retrieve the list of patients belonging to the doctor, sorted by ID in descending order
    patients = Patient.objects.filter(doctor_id=doctor_id).exclude(appointment__doctor_id=doctor_id).order_by('-id')
    context = {'patients': patients, 'doctor_id': doctor_id}
    return render(request, 'healthcare/Doctor_patient_list.html', context)



def appointment_page(request, doctor_id, patient_id):
    patient = Patient.objects.get(id=patient_id)
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'healthcare/Doctor_schedule.html', {'doctor': doctor, 'patient': patient})





def doctor_schedule(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        appointment_date = request.POST.get('appointment_time')
        
        # Convert the appointment date to a datetime object
        appointment_date = datetime.datetime.strptime(appointment_date, "%Y-%m-%dT%H:%M")
        
        # Adjust the appointment date (e.g., add/subtract hours or days as needed)
        corrected_appointment_date = appointment_date + datetime.timedelta(hours=3)  # Example: Add 3 hours
        
        message = f"Dear {patient.name}, this is a friendly reminder for your next appointment on {appointment_date} at KCMC hospital. Please arrive 30 Minutes before your appointment in order to avoid any circumstance that might delay the appointment with the doctor."
        Appointment.objects.create(doctor=doctor, patient=patient, appointment_date=corrected_appointment_date, message=message)
        return redirect('doctor_patient_list')  # replace with the name of the template or URL to redirect to after successful appointment creation
    else:
        return render(request, 'Doctor_schedle.html', {'doctor': doctor})



# def appointment_list(request, doctor_id):
#     # Fetch appointments for the specified doctor
#     appointments = Appointment.objects.filter(doctor_id=doctor_id)
#     return render(request, 'healthcare/Doctor_Appointment.html', {'appointments': appointments})




def appointment_list(request, doctor_id):
    # Fetch appointments for the specified doctor
    appointments = Appointment.objects.filter(doctor_id=doctor_id)
    
    # Pass the doctor_id to the template context
    return render(request, 'healthcare/Doctor_Appointment.html', {
        'appointments': appointments,
        'doctor_id': doctor_id  # Make sure this is included
    })

def contact(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'healthcare/Contact.html')