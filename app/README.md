AI Receptionist (MVP)
This is a simple AI Receptionist prototype 
I built to practice chabot and automation workflow.

Features

. Answerbasic FAQs (hours, Services, pricing)

. Handle simple chat conversations 

. Book appointments via Google Calendar 

. Built with FastAPI + Python

HOW IT WORKS

. User sends a message --> system checks if it matches an FAQ

. If booking is requested --> user provides date/time --> event is added to Google Calendar

. Fallback reply if the system dose't understand

Tech Stack

. Python, FasAPI, Pydantic
. Google Calendar API

Run locally

uvicorn app.main:app --reload

Open:http://127.0.0.1:8000/docs


Built as a learning + portfolio project.