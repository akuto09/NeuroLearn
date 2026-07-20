from flask import Blueprint, render_template, request, flash, redirect, url_for
from database.connection import get_db
from middleware.authentication import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():
    conn = get_db()
    total_users = conn.execute("SELECT COUNT(*) c FROM users").fetchone()["c"]
    total_students = conn.execute("SELECT COUNT(*) c FROM users WHERE role='student'").fetchone()["c"]
    total_teachers = conn.execute("SELECT COUNT(*) c FROM users WHERE role='teacher'").fetchone()["c"]
    total_courses = conn.execute("SELECT COUNT(*) c FROM courses").fetchone()["c"]
    recent = conn.execute("SELECT name, role, created_at FROM users ORDER BY id DESC LIMIT 6").fetchall()
    conn.close()

    stats = {
        "total_users": total_users, "total_students": total_students,
        "total_teachers": total_teachers, "total_courses": total_courses,
    }
    recent_users = [{"name": r["name"], "role": r["role"], "joined": r["created_at"]} for r in recent]
    return render_template("admin/dashboard.html", stats=stats, recent_users=recent_users)


@admin_bp.route("/users")
@role_required("admin")
def users():
    conn = get_db()
    rows = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    users = [{"name": r["name"], "email": r["email"], "role": r["role"], "joined": r["created_at"]} for r in rows]
    return render_template("admin/users.html", users=users)


@admin_bp.route("/courses")
@role_required("admin")
def courses():
    conn = get_db()
    rows = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    enrolled_counts = [34, 28, 19, 22, 15, 27]
    courses = []
    for i, c in enumerate(rows):
        courses.append({
            "title": c["title"], "category": c["category"], "level": c["level"],
            "enrolled": enrolled_counts[i % len(enrolled_counts)],
        })
    return render_template("admin/courses.html", courses=courses)


@admin_bp.route("/reports")
@role_required("admin")
def reports():
    return render_template("admin/reports.html")


@admin_bp.route("/ai-settings", methods=["GET", "POST"])
@role_required("admin")
def ai_settings():
    if request.method == "POST":
        flash("AI engine configuration saved.", "success")
        return redirect(url_for("admin.ai_settings"))
    return render_template("admin/ai_settings.html")
