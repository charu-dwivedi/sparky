
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import utils as utils

scopes = ['https://www.googleapis.com/auth/calendar']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'Spark Voice Assistant-dee7fd240faf.json', scopes=scopes)

http_auth = credentials.authorize(Http())

service = build('calendar', 'v3', http=http_auth)

def schedule(users, start, end):
    attendees = []
    for user in users:
        attendees.append({
            "email": user[1]
        })
    data = {
        "summary": "Followup Meeting",
        "description": "Let's reconvene to discuss this further",
        "start": {
            "dateTime": start,
            "timeZone": "America/Los_Angeles"
        },
        "end": {
            "dateTime": end,
            "timeZone": "America/Los_Angeles"
        },
        "attendees": attendees,
        "reminders": {
            "useDefault": True
        }
    }
    event = service.events().insert(calendarId='primary', sendNotifications=True, body=data).execute()
    print 'Event created: %s' % (event.get('htmlLink'))


schedule(utils.get_users(utils.developer_tokens['tanay'], "Y2lzY29zcGFyazovL3VzL1JPT00vNjJmZThkODAtMzE5MC0xMWU2LWJmYTUtNGI0NDY2NzI2MDM2"), "2016-06-14T18:00:00", "2016-06-14T18:30:00")