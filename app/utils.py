from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

def create_google_calendar_event(appointment):
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Load or perform OAuth flow
    try:
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    except (FileNotFoundError, ValueError):
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)

    timezone = 'Asia/Kolkata'
    start_time = f"{appointment.date}T{appointment.start_time}:00"
    end_time = f"{appointment.date}T{appointment.end_time}:00"

    event_body = {
        'summary': f"Appointment between {appointment.patient.first_name} and Dr. {appointment.doctor.first_name}",
        'start': {'dateTime': start_time, 'timeZone': timezone},
        'end': {'dateTime': end_time, 'timeZone': timezone},
        'attendees': [
            {'email': appointment.doctor.email},
            {'email': appointment.patient.email},
        ],
    }

    try:
        event = service.events().insert(calendarId='primary', body=event_body).execute()
        appointment.calendar_event_id = event.get('id')
        appointment.save()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Error creating event: {e}")






from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def delete_google_calendar_event(appointment):
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Load saved credentials or initiate OAuth flow
    credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=credentials)

    # Assuming the event ID is stored in the appointment model (e.g., appointment.calendar_event_id)
    if hasattr(appointment, 'calendar_event_id') and appointment.calendar_event_id:
        service.events().delete(calendarId='primary', eventId=appointment.calendar_event_id).execute()
