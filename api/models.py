from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone

class NurseManager(BaseUserManager):
    def create_user(self, email, name, IdNumber, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, IdNumber=IdNumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, IdNumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, IdNumber, password, **extra_fields)

class Nurse(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    IdNumber = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='nurse_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='nurse_permissions')

    objects = NurseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'IdNumber']

    class Meta:
        db_table = 'nurse'

class DoctorManager(BaseUserManager):
    def create_user(self, email, name, IdNumber, roomNo, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, IdNumber=IdNumber, roomNo=roomNo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, IdNumber, roomNo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, IdNumber, roomNo, password, **extra_fields)

class Doctor(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    IdNumber = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    roomNo = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='doctor_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='doctor_permissions')

    objects = DoctorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'IdNumber']

    class Meta:
        db_table = 'doctor'




class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    health_insurance = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'patient'


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    message = models.TextField()

    class Meta:
        unique_together = ('doctor', 'patient', 'appointment_date')
        db_table = 'appointment'

