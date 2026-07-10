#Click on this link to view my site 
https://career-compass-web-ygql.onrender.com

# Career Compass — Career Counselling & Guidance Mini Project

A simple full-stack app: students take an 8-question interest quiz and get a
career category recommendation; results are saved so a counsellor can review
them on a dashboard.

## Tech Stack
- **Backend:** FastAPI (Python) + SQLite
- **Frontend:** React + Vite

## Project Structure
```
career-compass/
├── backend/
│   ├── main.py            # All API logic (quiz data, scoring, DB)
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx         # Routes
        ├── api.js          # Talks to backend
        ├── index.css
        └── pages/
            ├── Home.jsx
            ├── Quiz.jsx
            ├── Result.jsx
            └── Dashboard.jsx
```

## How to Run

### 1. Backend (Terminal 1)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
This starts the API at `http://127.0.0.1:8000`.
A `career.db` SQLite file is created automatically on first run.

Check it works by visiting `http://127.0.0.1:8000/docs` — FastAPI's
auto-generated API test page.

### 2. Frontend (Terminal 2 — keep backend running)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

## How It Works
1. **Quiz** (`/quiz`): student enters their name, then answers 8 multiple
   choice questions. Each option is tagged with a career category
   (technology, arts, business, science, social).
2. On the last question, the frontend POSTs all answers to
   `/api/submit`. The backend counts how many times each category was
   picked, and the category with the highest count becomes the
   recommendation. The result is saved to SQLite.
3. **Result** (`/result`): shows the recommended category, suggested
   careers, next steps, and a simple bar breakdown of all category scores.
4. **Dashboard** (`/dashboard`): counsellors can see every student's name,
   class, recommended category, and submission date, pulled from
   `/api/dashboard`.

## Ideas to Extend (good for viva questions / report "future scope")
- Add login for students and counsellors (JWT auth)
- Let counsellors leave notes/feedback per student
- Weight questions differently instead of simple counting
- Add more categories and a longer, validated questionnaire
- Export dashboard results to Excel/PDF
- Deploy backend (Render/Railway) + frontend (Vercel/Netlify) for a live demo

## Notes for Your Report
This maps well onto a "Career Counselling and Guidance" mini project brief:
- **Problem:** Many school students choose streams/careers without
  structured guidance.
- **Solution:** A lightweight, low-cost digital tool that gives every
  student an instant, personalised starting point, and gives counsellors
  visibility into the whole student body's interests at a glance.
- **Scope:** This is a proof-of-concept — a real deployment would need a
  validated psychometric questionnaire (ideally designed with an actual
  counsellor) rather than the illustrative 8-question quiz here.
