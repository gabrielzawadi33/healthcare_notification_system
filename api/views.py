from venv import logger
from django.shortcuts import redirect, render
from .models import Doctor, Nurse, Patient
from .serializers import DoctorSerializers, NurseSerializers, PatientSerializer
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView


# Create your views here.

def home(request):
    return render(request, 'healthcare/Home_page.html')


###############################################################################################
def nurse_dashboard(request):
    doctors = Doctor.objects.all()
    return render(request, 'healthcare/Nurse_After_login.html', {'doctors': doctors})


from django.contrib.auth.hashers import make_password
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
                    # User is authenticated, you can log them in
                    request.session['user_id'] = user.id
                    logger.info(f'User {email} authenticated successfully')
                    return redirect('nurse_dashboard')
                else:
                    print(f'Input password: {password}')  # Debugging line  
                    print(f'Actual password: {user.password}')  # Debugging line
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


def signup_doctor(request):
    return render(request, 'healthcare/signup_doctor.html')
    

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
                    # User is authenticated, you can log them in
                    request.session['user_id'] = user.id
                    logger.info(f'User {email} authenticated successfully')
                    return redirect('doctor_dashboard')
                else:
                    print(f'Input password: {password}')  # Debugging line  
                    print(f'Actual password: {user.password}')  # Debugging line
                    messages.error(request, 'Invalid username or password.')
                    logger.warning(f'Failed to authenticate user {email}: Invalid password')
            except Doctor.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                logger.warning(f'Failed to authenticate user {email}: User does not exist')
    return render(request, 'healthcare/login_doctor.html')

def doctor_dashboard(request):
    patients = Patient.objects.filter(doctor_id=request.session['user_id'])
    patient_count = patients.count()
    print(patient_count)
    context = {'patients': patients, 
               'patient_count': patient_count}
    serializer = PatientSerializer(patients, many=True)
    return render(request, 'healthcare/Doctor_After_login.html', context)



class PatientsByDoctorView(APIView):
    def get(self, request, doctor_id, format=None):
        patients = Patient.objects.filter(doctor__id=doctor_id)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
    


def register_patient(request):
    if request.method == 'POST':
        name = request.POST['name']
        patient_id = request.POST['patient_id']
        address = request.POST['address']
        doctor_id = request.POST['doctor']
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        roomNo = request.POST['roomNo']  # assuming you have this field in your form

        # Fetch the doctor instance
        doctor = Doctor.objects.get(id=doctor_id)

        # Create a new patient
        patient = Patient(name=name, patient_id=patient_id, address=address, doctor=doctor, date_of_birth=date_of_birth, gender= gender)

        # Save the patient
        patient.save()

        messages.success(request, 'Patient registered successfully')
        return redirect('nurse_dashboard')  # replace with your redirect URL

    else:
        doctors = Doctor.objects.all()
        return render(request, 'Nurse_After_login.html', {'doctors': doctors})
    


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'healthcare/Nurse_patients_list.html', {'patients': patients})