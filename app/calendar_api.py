import datetime as dt
from typing import Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/ayth/calendar"]
def _get_service():
    creds = Credentials.from_authorized_user_file(
        os.getenv("GOOGLE_TOKEN_FILE","token.json"),
        SCOPES
    )
    service = build("calendar", "v3", credentials=creds)
    return service
def book_event(
    calendar_id: str,
    summary: str,
    description: str,
    start_iso: str,
    end_iso: str,
    attendee_email: Optional[str] = None
) -> str:
    service = _get_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_iso},
        "end": {"dateTime", end_iso},
    }
    if attendee_email:
        event["attendees"] = [{"email": attendee_email}]
        created = service.events().insert(calendarId=calendar_id, body=event).execute()
        return created.get("htmlLink", "")