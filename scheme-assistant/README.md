# Scheme Setu — AI-Based Personalized Government Scheme Eligibility Assistant

## What this is
A working MVP for the SIH problem statement: users enter basic demographic,
income, and education details and get a personalized, explainable list of
government schemes they're eligible for, plus step-by-step application
guidance. Built with a rule-based eligibility engine (fully explainable,
no black-box ML) demoed on 6 real-style education scholarship schemes.

## How to run it

1. Install Python 3.9+ if you don't have it.
2. Open a terminal in this folder and install Flask:
   pip install flask

3. Run the app:
   python3 app.py

4. Open your browser to:
   http://localhost:5000

## Project structure
- app.py                → Flask server, routes
- eligibility.py         → Rule-based matching engine (the "AI" logic)
- schemes.json           → Scheme database (add more schemes here)
- templates/index.html   → Form + results page
- static/style.css       → Styling
- static/script.js       → Frontend logic (form submit, rendering results)

## How to add more schemes
Open schemes.json and add a new object following the same structure as
the existing entries (age range, categories, income cap, education
levels, states, documents, application steps). No code changes needed —
the engine reads the file dynamically at every request.

## How the matching works
Each scheme has explicit rules (age range, category, income ceiling,
education level, state, gender, disability requirement). The engine
checks a user's profile against every rule for every scheme, giving a
match score out of 100%. Schemes with all criteria met go in "eligible."
Schemes at 70%+ with 1-2 missing criteria go in "close matches" so users
can see what they need to fix to qualify (e.g. get an income certificate
issued, wait until they turn 18, etc).

## Next steps for a full SIH submission
- Expand schemes.json to cover more domains (agriculture, health, housing)
- Add regional language support (Google Translate API)
- Add voice input for low-literacy users (Web Speech API)
- Add a document upload + OCR verification module (kept separate per
  scope decision — listed as future work in the problem statement)
- Replace the JSON file with a proper database once scheme count grows
- Connect to real Aadhaar/DigiLocker APIs for verified e-KYC (currently
  simulated via static application-step text)
