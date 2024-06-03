from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone # type: ignore
from .models import Appointment

@shared_task
def check_appointments():
    # Get the current time in UTC
    now = timezone.now()
    print(f"Current UTC time: {now}")
    
    # Convert UTC time to your local timezone
    tz = timezone.get_current_timezone()
    now_local = now.astimezone(tz)
    print(f"Current local time (Tanzania): {now_local}")
    
    upcoming_appointments = Appointment.objects.filter(appointment_date__range=(now_local, now_local + timezone.timedelta(hours=1)))
    if not upcoming_appointments:
        print("No upcoming appointments")
    else:
        for appointment in upcoming_appointments:
            print(f"Upcoming appointment: {appointment.id} at {appointment.appointment_date}")
