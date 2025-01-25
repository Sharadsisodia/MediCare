from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def create_google_calendar_event(appointment):
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Check if token.json exists (saved credentials)
    try:
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    except (FileNotFoundError, ValueError):
        # If no valid credentials are found, perform the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token_file:
            token_file.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)

    # Create the event details
    event = {
        'summary': f"Appointment with {appointment.doctor.first_name}",
        'start': {
            'dateTime': f"{appointment.date}T{appointment.start_time}:00Z",
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': f"{appointment.date}T{appointment.end_time}:00Z",
            'timeZone': 'UTC',
        },
        'attendees': [{'email': appointment.doctor.email}],
    }

    try:
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        appointment.calendar_event_id = event_result.get('id')  # Save the event ID
        appointment.save()
        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")




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
