from __future__ import absolute_import, unicode_literals
from api.utils import send_sms_via_beem
from celery import shared_task
from django.utils import timezone  # type: ignore
from .models import Appointment
import datetime

@shared_task
def check_appointments():
    # Get the current time in UTC
    now = timezone.now() + timezone.timedelta(hours=3)

    one_hour_later = now + timezone.timedelta(hours=1)
    
    # Log the current time and the one hour later time in UTC
    print(f"Checking for appointments between {now} and {one_hour_later} UTC")

    # Find appointments within the next hour (in UTC)
    upcoming_appointments = Appointment.objects.filter(appointment_date__range=(now, one_hour_later))
    
    if not upcoming_appointments:
        print("No upcoming appointments")
    else:
        for appointment in upcoming_appointments:
            # Convert the appointment date to local timezone for display purposes
            tz = timezone.get_current_timezone()
            appointment_date_local = appointment.appointment_date.astimezone(tz)
            print('___________________________________________________________________________________________________')
            print(f"Upcoming appointment: {appointment.id} at {appointment_date_local}")
            print(f"Appointment UTC time: {appointment.appointment_date}")
            print(f"Current local time (Tanzania): {now.astimezone(tz)}")
            print(f"Current UTC time: {now}")
            print('______________________________________________________________________________________________________')
            
            body = appointment.message
            to = appointment.patient.phone_number
            
            print(body)
            send_sms_via_beem(body, to)
