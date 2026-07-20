from flask import Blueprint, render_template
from middleware.authentication import role_required

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")


@teacher_bp.route("/dashboard")
@role_required("teacher")
def dashboard():
    stats = {"students": 42, "avg_attention": 63, "avg_fatigue": 28, "courses": 3}
    flagged = [
        {"name": "Riya Nair", "course": "Advanced Calculus", "attention": 31, "fatigue": 71, "flag": "Fatigued", "pill": "pill-rose"},
        {"name": "Tom Alvarez", "course": "Applied ML", "attention": 38, "fatigue": 58, "flag": "Distracted", "pill": "pill-amber"},
        {"name": "Chidi Okoye", "course": "Advanced Calculus", "attention": 44, "fatigue": 66, "flag": "Fatigued", "pill": "pill-rose"},
    ]
    return render_template("teacher/dashboard.html", stats=stats, flagged=flagged)


@teacher_bp.route("/students")
@role_required("teacher")
def students():
    students = [
        {"name": "Riya Nair", "course": "Advanced Calculus", "mastery": 54, "last_active": "2 hours ago"},
        {"name": "Tom Alvarez", "course": "Applied ML", "mastery": 68, "last_active": "1 day ago"},
        {"name": "Chidi Okoye", "course": "Advanced Calculus", "mastery": 47, "last_active": "3 hours ago"},
        {"name": "Mei Tanaka", "course": "Applied ML", "mastery": 91, "last_active": "20 min ago"},
        {"name": "Sam Carter", "course": "Advanced Calculus", "mastery": 76, "last_active": "5 min ago"},
    ]
    return render_template("teacher/students.html", students=students)


@teacher_bp.route("/courses")
@role_required("teacher")
def courses():
    courses = [
        {"title": "Advanced Calculus", "students": 21, "description": "Limits, derivatives, and integrals with adaptive pacing."},
        {"title": "Applied Machine Learning", "students": 18, "description": "Core ML concepts with hands-on adaptive exercises."},
        {"title": "Foundations of Neuroscience", "students": 15, "description": "How the brain builds memory and attention."},
    ]
    return render_template("teacher/courses.html", courses=courses)
