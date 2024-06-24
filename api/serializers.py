from django.contrib.auth.hashers import make_password # type: ignore
from django.db import IntegrityError # type: ignore
from rest_framework import serializers # type: ignore
from .models import Appointment, Doctor, Nurse, Patient




class NurseSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Nurse
        fields = ['name', 'IdNumber', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Nurse.objects.create(**validated_data) 


class DoctorSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['name', 'IdNumber', 'email', 'password', 'roomNo']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Doctor.objects.create(**validated_data)
    

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerualizer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'