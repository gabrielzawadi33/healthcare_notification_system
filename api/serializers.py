from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from rest_framework import serializers
from .models import Doctor, Nurse



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
    


# serializers.py
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


