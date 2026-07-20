from flask import Blueprint, render_template, request, flash, redirect, url_for
from database.connection import get_db

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    return render_template("public/home.html")


@public_bp.route("/about")
def about():
    return render_template("public/about.html")


@public_bp.route("/features")
def features():
    return render_template("public/features.html")


@public_bp.route("/courses")
def courses():
    conn = get_db()
    rows = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("public/courses.html", courses=rows)


@public_bp.route("/pricing")
def pricing():
    return render_template("public/pricing.html")


@public_bp.route("/faq")
def faq():
    return render_template("public/faq.html")


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please fill in every field.", "error")
            return redirect(url_for("public.contact"))
        conn = get_db()
        conn.execute(
            "INSERT INTO contact_messages (name, email, message) VALUES (?,?,?)",
            (name, email, message),
        )
        conn.commit()
        conn.close()
        flash("Thanks — your message has been sent. We'll reply within two business days.", "success")
        return redirect(url_for("public.contact"))
    return render_template("public/contact.html")
