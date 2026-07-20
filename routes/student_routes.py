from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from database.connection import get_db
from middleware.authentication import role_required
from ai_engine import eeg_processing

student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.route("/dashboard")
@role_required("student")
def dashboard():
    conn = get_db()
    courses = conn.execute("SELECT * FROM courses LIMIT 3").fetchall()
    conn.close()

    active_courses = [
        {"title": c["title"], "progress": p}
        for c, p in zip(courses, [72, 45, 30])
    ]

    upcoming = [
        {
            "title": "Chapter 4 Quiz",
            "course": "Applied Machine Learning",
            "due": "Tomorrow, 6:00 PM",
            "status": "Pending",
            "pill": "pill-amber",
        },
        {
            "title": "Essay Draft",
            "course": "English Composition",
            "due": "Fri, Jul 24",
            "status": "Not started",
            "pill": "pill-rose",
        },
        {
            "title": "Unit 2 Problem Set",
            "course": "Advanced Calculus",
            "due": "Mon, Jul 27",
            "status": "In progress",
            "pill": "pill-blue",
        },
    ]

    return render_template(
        "student/dashboard.html",
        active_courses=active_courses,
        upcoming=upcoming,
    )


@student_bp.route("/courses")
@role_required("student")
def courses():
    conn = get_db()
    rows = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()

    progress_values = [72, 45, 30, 88, 12, 60]

    courses_data = []

    for i, c in enumerate(rows):
        courses_data.append(
            {
                "title": c["title"],
                "category": c["category"],
                "description": c["description"],
                "progress": progress_values[i % len(progress_values)],
            }
        )

    return render_template("student/courses.html", courses=courses_data)


@student_bp.route("/assignments")
@role_required("student")
def assignments():

    assignments = [
        {
            "title": "Chapter 4 Quiz",
            "course": "Applied Machine Learning",
            "due": "Jul 19",
            "status": "Pending",
            "pill": "pill-amber",
        },
        {
            "title": "Essay Draft",
            "course": "English Composition",
            "due": "Jul 24",
            "status": "Not started",
            "pill": "pill-rose",
        },
        {
            "title": "Unit 2 Problem Set",
            "course": "Advanced Calculus",
            "due": "Jul 27",
            "status": "In progress",
            "pill": "pill-blue",
        },
        {
            "title": "Lab Report 3",
            "course": "Foundations of Neuroscience",
            "due": "Jul 30",
            "status": "Completed",
            "pill": "pill-green",
        },
    ]

    return render_template(
        "student/assignments.html",
        assignments=assignments,
    )


@student_bp.route("/tests")
@role_required("student")
def tests():

    tests = [
        {
            "title": "ML Fundamentals Check",
            "description": "Adaptive quiz covering supervised learning basics.",
            "difficulty": "Standard",
            "tag_class": "on-attention",
            "questions": 15,
            "duration": "20 min",
        },
        {
            "title": "Calculus Diagnostic",
            "description": "Recalibrates difficulty as you answer.",
            "difficulty": "Adaptive",
            "tag_class": "on-load",
            "questions": 12,
            "duration": "18 min",
        },
        {
            "title": "Neuroscience Review",
            "description": "Spaced-repetition review of prior modules.",
            "difficulty": "Review",
            "tag_class": "on-meditation",
            "questions": 10,
            "duration": "12 min",
        },
    ]

    return render_template(
        "student/tests.html",
        tests=tests,
    )


@student_bp.route("/progress")
@role_required("student")
def progress():

    weekly_chart = []

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    attn = [60, 68, 55, 72, 64, 40, 35]
    fat = [20, 25, 30, 22, 35, 45, 50]

    x = 10

    for i, d in enumerate(days):
        weekly_chart.append(
            {
                "x": x,
                "day": d,
                "attention": attn[i],
                "fatigue": fat[i],
            }
        )
        x += 80

    mastery = [
        {"title": "Applied Machine Learning", "value": 72},
        {"title": "Advanced Calculus", "value": 45},
        {"title": "Foundations of Neuroscience", "value": 88},
    ]

    return render_template(
        "student/progress.html",
        weekly_chart=weekly_chart,
        mastery=mastery,
    )


@student_bp.route("/ai-assistant")
@role_required("student")
def ai_assistant():
    return render_template("student/ai_assistant.html")


@student_bp.route("/meditation")
@role_required("student")
def meditation():

    key = f"user-{session.get('user_id')}"

    raw = eeg_processing.read_mental_state(key)

    attention = raw["attention"]
    fatigue = raw["fatigue"]
    cognitive_load = raw["cognitive_load"]

    if attention < 40:
        recommendation = "Your attention level appears low."
        session_text = (
            "A 3-minute Focus Breathing session is recommended before continuing your studies."
        )

    elif fatigue > 70:
        recommendation = "You seem mentally fatigued."
        session_text = "Take a 5-minute Relaxation session."

    elif cognitive_load > 80:
        recommendation = "Your cognitive load is high."
        session_text = "Practice a Mindfulness session before studying."

    else:
        recommendation = "You're mentally ready to continue learning."
        session_text = "A short 2-minute breathing exercise is optional."

    return render_template(
        "student/meditation.html",
        recommendation=recommendation,
        session=session_text,
    )


@student_bp.route("/settings", methods=["GET", "POST"])
@role_required("student")
def settings():

    if request.method == "POST":

        new_name = request.form.get("name", "").strip()

        if new_name:
            conn = get_db()
            conn.execute(
                "UPDATE users SET name = ? WHERE id = ?",
                (new_name, session["user_id"]),
            )
            conn.commit()
            conn.close()

            session["name"] = new_name

            flash("Settings saved.", "success")

        return redirect(url_for("student.settings"))

    return render_template("student/settings.html")