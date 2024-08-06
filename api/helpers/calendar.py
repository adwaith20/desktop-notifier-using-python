from google.oauth2 import service_account
import googleapiclient.discovery

# Load credentials from JSON service account key file
credentials = service_account.Credentials.from_service_account_file(
    'client_secret_938294709733-jbn0emc6aemlm2o6q4qa3ja22h59k770.apps.googleusercontent.com.json',
    scopes=['https://www.googleapis.com/auth/calendar.readonly']
)

# Create a Google Calendar API service object
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

# Example: List all events in the primary calendar
events_result = service.events().get(calendarId='primary', maxResults=10).execute()
events = events_result.get('items', [])



# event = service.events().get(calendarId='primary', eventId='eventId').execute()

print (events['summary'])
if not events:
    print('No upcoming events found.')
else:
    print('Upcoming events:')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f'{start} - {event["summary"]}')
