"""
Career Compass - Backend
A simple FastAPI server that:
1. Serves a career-interest quiz
2. Scores answers and recommends a career category
3. Saves every result to a SQLite database
4. Lets a counsellor view all past results on a dashboard
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

app = FastAPI(title="Career Compass API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "career.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_class TEXT,
            category TEXT NOT NULL,
            scores TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()

# ---------------------------------------------------------------------------
# Quiz data: each question has 4 options, each option is tagged with a
# career category. We simply count how many times each category is chosen.
# ---------------------------------------------------------------------------

QUESTIONS = [
    {
        "id": 1,
        "text": "Which activity sounds most fun to you?",
        "options": [
            {"label": "Building or fixing a gadget", "category": "technology"},
            {"label": "Drawing, designing, or making music", "category": "arts"},
            {"label": "Planning an event or running a small stall", "category": "business"},
            {"label": "Helping a friend understand a topic", "category": "social"},
        ],
    },
    {
        "id": 2,
        "text": "In a group project, you naturally end up:",
        "options": [
            {"label": "Writing the code / solving the technical part", "category": "technology"},
            {"label": "Designing the slides or the look of the project", "category": "arts"},
            {"label": "Organizing the team and deadlines", "category": "business"},
            {"label": "Making sure everyone is included and happy", "category": "social"},
        ],
    },
    {
        "id": 3,
        "text": "Which school subject do you enjoy the most?",
        "options": [
            {"label": "Maths / Computer Science", "category": "technology"},
            {"label": "Art / Literature / Music", "category": "arts"},
            {"label": "Economics / Commerce", "category": "business"},
            {"label": "Biology / Chemistry (life sciences)", "category": "science"},
        ],
    },
    {
        "id": 4,
        "text": "Your ideal weekend project would be:",
        "options": [
            {"label": "Building a small app or website", "category": "technology"},
            {"label": "Painting, editing videos, or writing a story", "category": "arts"},
            {"label": "Starting a small side hustle", "category": "business"},
            {"label": "Volunteering at an NGO or teaching kids", "category": "social"},
        ],
    },
    {
        "id": 5,
        "text": "Which of these questions interests you the most?",
        "options": [
            {"label": "How does this app/website actually work?", "category": "technology"},
            {"label": "What makes this design/song/story beautiful?", "category": "arts"},
            {"label": "How can this product be sold better?", "category": "business"},
            {"label": "How does the human body / nature work?", "category": "science"},
        ],
    },
    {
        "id": 6,
        "text": "Pick a TV/YouTube genre you'd binge:",
        "options": [
            {"label": "Tech reviews / coding tutorials", "category": "technology"},
            {"label": "Art, film-making, or music channels", "category": "arts"},
            {"label": "Startup stories / stock market", "category": "business"},
            {"label": "Documentaries on medicine or space", "category": "science"},
        ],
    },
    {
        "id": 7,
        "text": "Which achievement would make you proudest?",
        "options": [
            {"label": "Building software used by many people", "category": "technology"},
            {"label": "Creating something people find beautiful", "category": "arts"},
            {"label": "Growing a business or brand", "category": "business"},
            {"label": "Helping someone overcome a real problem", "category": "social"},
        ],
    },
    {
        "id": 8,
        "text": "Which work environment appeals to you most?",
        "options": [
            {"label": "A tech lab surrounded by computers", "category": "technology"},
            {"label": "A creative studio", "category": "arts"},
            {"label": "A hospital or research lab", "category": "science"},
            {"label": "A school, NGO, or community center", "category": "social"},
        ],
    },
]

# Info shown to the student based on their top category
CAREER_INFO = {
    "technology": {
        "title": "Technology & Engineering",
        "description": (
            "You enjoy logical problem-solving and building things. "
            "You'd likely thrive in fields that combine creativity with technical skill."
        ),
        "careers": [
            "Software Engineer",
            "Data Scientist / AI Engineer",
            "Cybersecurity Analyst",
            "Cloud / DevOps Engineer",
            "Robotics Engineer",
        ],
        "next_steps": [
            "Learn a programming language (Python/JS) and Git",
            "Build 2-3 small personal projects",
            "Try a free intro course on AWS/Azure/GCP",
        ],
    },
    "arts": {
        "title": "Arts, Design & Media",
        "description": (
            "You think visually and enjoy self-expression. "
            "Careers that let you create and communicate will suit you well."
        ),
        "careers": [
            "UI/UX Designer",
            "Graphic Designer",
            "Film Maker / Video Editor",
            "Content Creator",
            "Architect",
        ],
        "next_steps": [
            "Build a portfolio (Behance/Instagram)",
            "Learn a design tool like Figma or Photoshop",
            "Take on freelance/college design projects",
        ],
    },
    "business": {
        "title": "Business & Management",
        "description": (
            "You like organizing, leading, and thinking about strategy and money. "
            "Business-oriented roles will let you use these strengths."
        ),
        "careers": [
            "Business Analyst",
            "Product Manager",
            "Entrepreneur",
            "Marketing Manager",
            "Financial Analyst",
        ],
        "next_steps": [
            "Read about a startup/business case study every week",
            "Try running a small club event or online store",
            "Learn basic Excel / Power BI",
        ],
    },
    "science": {
        "title": "Science & Healthcare",
        "description": (
            "You're curious about how the natural world and the human body work. "
            "Research and healthcare paths could be very fulfilling for you."
        ),
        "careers": [
            "Doctor / Medical Researcher",
            "Biotechnologist",
            "Pharmacist",
            "Data Analyst in Healthcare",
            "Environmental Scientist",
        ],
        "next_steps": [
            "Do a science fair or research mini-project",
            "Read popular science (articles, journals)",
            "Look into NEET / biology-focused electives if in school",
        ],
    },
    "social": {
        "title": "Social Service & Education",
        "description": (
            "You care about people and enjoy helping others grow. "
            "Careers built around teaching, guidance, or community impact will suit you."
        ),
        "careers": [
            "Teacher / Professor",
            "Career Counsellor",
            "Psychologist",
            "NGO / Social Worker",
            "HR Manager",
        ],
        "next_steps": [
            "Volunteer at a local NGO or teach juniors",
            "Read about psychology/education basics",
            "Practice public speaking or mentoring",
        ],
    },
}


class Answer(BaseModel):
    question_id: int
    category: str


class QuizSubmission(BaseModel):
    student_name: str
    student_class: str = ""
    answers: List[Answer]


@app.get("/")
def root():
    return {"message": "Career Compass API is running"}


@app.get("/api/questions")
def get_questions():
    return QUESTIONS


@app.post("/api/submit")
def submit_quiz(submission: QuizSubmission):
    if not submission.answers:
        raise HTTPException(status_code=400, detail="No answers submitted")

    scores = {}
    for ans in submission.answers:
        scores[ans.category] = scores.get(ans.category, 0) + 1

    top_category = max(scores, key=scores.get)
    info = CAREER_INFO.get(top_category)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO results (student_name, student_class, category, scores, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            submission.student_name,
            submission.student_class,
            top_category,
            str(scores),
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    conn.close()

    return {
        "category": top_category,
        "scores": scores,
        "info": info,
    }


@app.get("/api/dashboard")
def get_dashboard():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT id, student_name, student_class, category, created_at "
        "FROM results ORDER BY id DESC"
    )
    rows = c.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "student_name": r[1],
            "student_class": r[2],
            "category": r[3],
            "created_at": r[4],
        }
        for r in rows
    ]
