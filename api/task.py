from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from .models import Appointment

@shared_task
def check_appointments():
    print('ello')
    now = timezone.now()
    upcoming_appointments = Appointment.objects.filter(appointment_date__range=(now, now + timezone.timedelta(hours=1)))
    if not upcoming_appointments:
        print("No upcoming appointments")
    else:
        for appointment in upcoming_appointments:
            print(f"Upcoming appointment: {appointment.id} at {appointment.appointment_date}")