from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.config import load_client_config
from app.faq import answer_faq
from app.calendar_api import book_event
import os, datetime as dt

app = FastAPI(title="AI Receptionist MVP")

class ChatRequest(BaseModel):
    message: str
    client: str | None = None
    email: str | None = None
    
class BookRequest(BaseModel):
    client: str | None = None
    email: str | None = None
    date: str # "2025-08-25"
    start_time: str # "14:30"
    duration_min: int = 30
    note: str | None = None
    
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    client_key = req.client or os.getenv("DEFAULT_CLIENT", "default")
    cfg = load_client_config(client_key)
    
    ans = answer_faq(req.message, cfg)
    if ans:
        return {"reply": ans, "type": "faq"}
    
    if any(k in req.message.lower() for k in ["book", "appointment", "schedule"]):
        return {
            "reply": "Sure - please share a date (YYYY-MM-DD), start time (HH:MM), and your email.", 
            "type": "booking_prompt"
        }
    return {"reply": "I can help with hours, services, pricing, and booking appointments.", "type": "fallback"}

@app.post("/book")
def book(req: BookRequest):
    client_key = req.client or os.getenv("DEFAULT_CLIENT", "default")
    cfg = load_client_config(client_key)
    cal_id = cfg.get("calendar", {}).get("calendar_id", os.getenv("GOOGLE_CALENDAR_ID", "primary"))
    
    start_iso = f"{req.date}T{req.start_time}:00"
    start_dt = dt.datetime.fromisoformat(start_iso)
    end_dt = start_dt + dt.timedelta(minutes=req.duration_min)
    link = book_event(
        calendar_id=cal_id,
        summary=f"Appointment({cfg.get('name','Client')})", description=req.note or "Booked via AI Receptionist",
        start_iso=start_dt.isoformat(),
        end_iso=end_dt.isoformat(),
        attendee_email=req.email
    )
    return {"status": "booked", "calendar_link": link}
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "AI Receptionist API is running"}

@app.get("/faq")
def get_faq():
    return {
        "hours": "Mon-Fri: 9:00-17:00, Sat: 10:00-14:00",
        "services": "Consultation,Follow-ups, Nutrition Guidance", 
        "pricing": "Consultation $49, Follow-up $29"
    }
@app.get("/calendar")
def get_calendar():
    return {"calendar_id": "primary",
            "status": "connected"}