from werkzeug.security import generate_password_hash
from database.connection import get_db

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student','teacher','admin')),
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    level TEXT,
    description TEXT,
    modules INTEGER DEFAULT 6
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    progress INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, email TEXT, message TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cognitive_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    attention INTEGER, meditation INTEGER, cognitive_load INTEGER, fatigue INTEGER,
    recorded_at TEXT DEFAULT (datetime('now'))
);
"""

DEMO_COURSES = [
    ("Foundations of Neuroscience", "Science", "Beginner", "How the brain builds memory, attention, and learning circuits.", 8),
    ("Applied Machine Learning", "Technology", "Intermediate", "Core ML concepts with hands-on adaptive-difficulty exercises.", 10),
    ("Advanced Calculus", "Mathematics", "Advanced", "Limits, derivatives, and integrals paced to your cognitive load.", 12),
    ("English Composition", "Language", "Beginner", "Structured writing practice with fatigue-aware session lengths.", 6),
    ("Data Structures & Algorithms", "Technology", "Intermediate", "Core CS fundamentals with adaptive test difficulty.", 9),
    ("Competitive Exam Reasoning", "Test Prep", "Advanced", "High-volume practice tuned to overload thresholds.", 14),
]


def init_db(app):
    with app.app_context():
        conn = get_db()
        conn.executescript(SCHEMA)
        conn.commit()

        # seed demo courses
        count = conn.execute("SELECT COUNT(*) c FROM courses").fetchone()["c"]
        if count == 0:
            conn.executemany(
                "INSERT INTO courses (title, category, level, description, modules) VALUES (?,?,?,?,?)",
                DEMO_COURSES,
            )
            conn.commit()

        # seed demo admin account
        existing = conn.execute("SELECT id FROM users WHERE email = ?", ("admin@neurolearn.ai",)).fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?,?,?,?)",
                ("Admin User", "admin@neurolearn.ai", generate_password_hash("admin123"), "admin"),
            )
            conn.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?,?,?,?)",
                ("Dr. Ada Reyes", "teacher@neurolearn.ai", generate_password_hash("teacher123"), "teacher"),
            )
            conn.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?,?,?,?)",
                ("Sam Carter", "student@neurolearn.ai", generate_password_hash("student123"), "student"),
            )
            conn.commit()
        conn.close()
