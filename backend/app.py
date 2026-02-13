import os
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path
from functools import wraps

from flask import Flask, jsonify, request, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from sqlalchemy import or_, func
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("EDUGLOW_SECRET_KEY", "dev-secret-key-change")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATA_DIR / 'eduglow.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True

CORS(app, supports_credentials=True, origins=["https://eduglow1512.netlify.app"])
db = SQLAlchemy(app)

APP_BASE_URL = os.environ.get("EDUGLOW_BASE_URL", "http://127.0.0.1:5000")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    name = db.Column(db.String(120), nullable=True)
    subject = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    price = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_public(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "name": self.name,
            "subject": self.subject,
            "rating": self.rating,
            "price": self.price,
            "city": self.city,
            "image": self.image,
        }


class TeacherSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)


class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    level = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    price = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(255), nullable=False)


class TrialRequest(db.Model):
    __tablename__ = "trial_request"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subject = db.Column(db.String(120), nullable=True)
    price = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="requested")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def login_required(role=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = session.get("user_id")
            if not user_id:
                return jsonify({"error": "unauthorized"}), 401
            if role and session.get("role") != role:
                return jsonify({"error": "forbidden"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def ensure_schema():
    with db.engine.begin() as conn:
        columns = [row[1] for row in conn.execute(text("PRAGMA table_info(trial_request)")).fetchall()]
        if "user_id" not in columns:
            conn.execute(text("ALTER TABLE trial_request ADD COLUMN user_id INTEGER"))
        booking_columns = [row[1] for row in conn.execute(text("PRAGMA table_info(booking)")).fetchall()]
        if booking_columns:
            if "phone" not in booking_columns:
                conn.execute(text("ALTER TABLE booking ADD COLUMN phone TEXT"))


def send_email(to_email, subject, text_body, html_body=None):
    host = os.environ.get("EDUGLOW_SMTP_HOST")
    port = int(os.environ.get("EDUGLOW_SMTP_PORT", "587"))
    user = os.environ.get("EDUGLOW_SMTP_USER")
    password = os.environ.get("EDUGLOW_SMTP_PASS")
    from_email = os.environ.get("EDUGLOW_SMTP_FROM", user)
    use_tls = os.environ.get("EDUGLOW_SMTP_TLS", "true").lower() in {"1", "true", "yes"}

    if not host or not from_email:
        raise RuntimeError("SMTP not configured")

    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(text_body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(host, port) as server:
        if use_tls:
            server.starttls()
        if user and password:
            server.login(user, password)
        server.send_message(msg)


def seed_data():
    if Tutor.query.count() == 0:
        tutors = [
            Tutor(name="Priya Sharma", subject="Mathematics", level="Class 9-12", rating=4.9, price="INR 600/hr", city="Delhi", image="http://static.photos/people/200x200/1"),
            Tutor(name="Rohan Verma", subject="Physics", level="Class 11-12", rating=4.8, price="INR 700/hr", city="Delhi", image="http://static.photos/people/200x200/2"),
            Tutor(name="Neha Gupta", subject="English", level="All", rating=4.7, price="INR 450/hr", city="Bengaluru", image="http://static.photos/people/200x200/3"),
            Tutor(name="Amit Joshi", subject="Chemistry", level="Class 9-12", rating=4.6, price="INR 550/hr", city="Mumbai", image="http://static.photos/people/200x200/4"),
            Tutor(name="Sakshi Rao", subject="Computer Science", level="College", rating=4.8, price="INR 800/hr", city="Kolkata", image="http://static.photos/people/200x200/5"),
            Tutor(name="Vikram Patel", subject="Maths", level="Class 6-10", rating=4.5, price="INR 300/hr", city="Delhi", image="http://static.photos/people/200x200/6"),
        ]
        db.session.add_all(tutors)

    if User.query.filter_by(email="teacher@example.com").first() is None:
        teacher = User(
            email="teacher@example.com",
            password_hash=generate_password_hash("password123"),
            role="teacher",
            name="John Doe",
            subject="Mathematics",
            rating=4.8,
            price="INR 600/hr",
            city="Delhi",
            image="http://static.photos/people/200x200/10",
        )
        db.session.add(teacher)
        db.session.flush()
        skills = [
            TeacherSkill(teacher_id=teacher.id, name="Algebra"),
            TeacherSkill(teacher_id=teacher.id, name="Calculus"),
            TeacherSkill(teacher_id=teacher.id, name="Trigonometry"),
        ]
        db.session.add_all(skills)

    if User.query.filter_by(email="student@example.com").first() is None:
        student = User(
            email="student@example.com",
            password_hash=generate_password_hash("password123"),
            role="student",
            name="Student User",
        )
        db.session.add(student)

    db.session.commit()


with app.app_context():
    db.create_all()
    ensure_schema()
    seed_data()


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/auth/register")
def register():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    role = payload.get("role") or "student"
    name = payload.get("name")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if role not in {"student", "teacher"}:
        return jsonify({"error": "invalid role"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 400

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        name=name,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "registered", "user": user.to_public()})


@app.post("/api/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    role = payload.get("role")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401
    if role and user.role != role:
        return jsonify({"error": "role mismatch"}), 403

    session["user_id"] = user.id
    session["role"] = user.role
    return jsonify({"message": "logged_in", "user": user.to_public()})


@app.post("/api/auth/logout")
def logout():
    session.clear()
    return jsonify({"message": "logged_out"})


@app.get("/api/me")
@login_required()
def me():
    user = db.session.get(User, session["user_id"])
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify({"user": user.to_public()})


@app.post("/api/auth/forgot")
def forgot_password():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "email not found"}), 404
    token = secrets.token_urlsafe(24)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    PasswordResetToken.query.filter_by(user_id=user.id).delete()
    db.session.add(PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at))
    db.session.commit()
    reset_link = f"{APP_BASE_URL}/reset/{token}"
    text_body = (
        "You requested a password reset for EduGlow.\n"
        f"Reset link: {reset_link}\n"
        "This link expires in 1 hour."
    )
    html_body = (
        "<p>You requested a password reset for EduGlow.</p>"
        f"<p><a href=\"{reset_link}\">Reset your password</a></p>"
        "<p>This link expires in 1 hour.</p>"
    )
    try:
        send_email(user.email, "EduGlow password reset", text_body, html_body)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify({"message": "reset_email_sent"})


@app.post("/api/auth/reset")
def reset_password():
    payload = request.get_json(silent=True) or {}
    token = payload.get("token") or ""
    new_password = payload.get("new_password") or ""
    if not token or not new_password:
        return jsonify({"error": "token and new_password required"}), 400

    record = PasswordResetToken.query.filter_by(token=token).first()
    if not record or record.expires_at < datetime.utcnow():
        return jsonify({"error": "invalid or expired token"}), 400

    user = db.session.get(User, record.user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    user.password_hash = generate_password_hash(new_password)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "password_updated"})


@app.get("/api/tutors")
def list_tutors():
    tutors = Tutor.query.all()
    teachers = User.query.filter_by(role="teacher").all()
    teacher_ids = [t.id for t in teachers]
    skills_map = {}
    if teacher_ids:
        rows = TeacherSkill.query.filter(TeacherSkill.teacher_id.in_(teacher_ids)).all()
        for row in rows:
            skills_map.setdefault(row.teacher_id, []).append(row.name)
    return jsonify(
        {
            "tutors": (
                [
                    {
                        "id": t.id,
                        "name": t.name,
                        "subject": t.subject,
                        "level": t.level,
                        "rating": t.rating,
                        "price": t.price,
                        "city": t.city,
                        "image": t.image,
                        "skills": [],
                    }
                    for t in tutors
                ]
                + [
                    {
                        "id": f"teacher-{t.id}",
                        "name": t.name or "Teacher",
                        "subject": t.subject or "Subject",
                        "level": ", ".join(skills_map.get(t.id, [])) or "All levels",
                        "rating": t.rating or 4.5,
                        "price": t.price or "INR 500/hr",
                        "city": t.city or "City",
                        "image": t.image or "http://static.photos/people/200x200/10",
                        "skills": skills_map.get(t.id, []),
                    }
                    for t in teachers
                ]
            )
        }
    )


@app.post("/api/trials")
def create_trial():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    phone = payload.get("phone")
    subject = payload.get("subject")
    if not name or not phone or not subject:
        return jsonify({"error": "name, phone, and subject required"}), 400
    clean_phone = str(phone).replace(" ", "").replace("-", "").replace("+", "")
    if not clean_phone.isdigit():
        return jsonify({"error": "phone must be numeric"}), 400
    trial = TrialRequest(
        name=name,
        phone=clean_phone,
        subject=subject,
        user_id=session.get("user_id"),
    )
    db.session.add(trial)
    db.session.commit()
    return jsonify({"message": "trial_submitted"})


@app.post("/api/bookings")
@login_required(role="student")
def create_booking():
    payload = request.get_json(silent=True) or {}
    teacher_id = payload.get("teacher_id")
    subject = payload.get("subject")
    phone = (payload.get("phone") or "").strip()
    if not teacher_id:
        return jsonify({"error": "teacher_id required"}), 400
    if not phone:
        return jsonify({"error": "phone required"}), 400
    if not phone.replace(" ", "").replace("-", "").replace("+", "").isdigit():
        return jsonify({"error": "phone must be numeric"}), 400
    teacher = User.query.filter_by(id=teacher_id, role="teacher").first()
    if not teacher:
        return jsonify({"error": "teacher not found"}), 404

    booking = Booking(
        student_id=session["user_id"],
        teacher_id=teacher.id,
        subject=subject or teacher.subject or "General",
        price=teacher.price or "INR 500/hr",
        phone=phone,
        status="requested",
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "booking_created", "booking_id": booking.id})


@app.get("/api/teacher/bookings")
@login_required(role="teacher")
def teacher_bookings():
    teacher_id = session["user_id"]
    bookings = Booking.query.filter_by(teacher_id=teacher_id).order_by(Booking.created_at.desc()).all()
    students = {u.id: u for u in User.query.filter(User.id.in_([b.student_id for b in bookings])).all()}
    return jsonify(
        {
            "bookings": [
                {
                    "id": b.id,
                    "subject": b.subject,
                    "price": b.price,
                    "status": b.status,
                    "created_at": f"{b.created_at.isoformat()}Z",
                    "student_name": students.get(b.student_id).name if students.get(b.student_id) else "Student",
                    "student_email": students.get(b.student_id).email if students.get(b.student_id) else "",
                    "student_phone": b.phone or "",
                }
                for b in bookings
            ]
        }
    )


@app.get("/api/teacher/trials")
@login_required(role="teacher")
def teacher_trials():
    teacher = db.session.get(User, session["user_id"])
    skills = [s.name for s in TeacherSkill.query.filter_by(teacher_id=teacher.id).all()]
    terms = []
    if teacher.subject:
        terms.append(teacher.subject)
    terms.extend(skills)
    terms = [t.strip() for t in terms if t and t.strip()]

    if not terms:
        return jsonify({"trials": []})

    conditions = []
    for term in terms:
        like = f"%{term.lower()}%"
        conditions.append(func.lower(TrialRequest.subject).like(like))

    trials = TrialRequest.query.filter(or_(*conditions)).order_by(TrialRequest.created_at.desc()).all()
    students = {u.id: u for u in User.query.filter(User.id.in_([t.user_id for t in trials if t.user_id])).all()}
    return jsonify(
        {
            "trials": [
                {
                    "id": t.id,
                    "subject": t.subject,
                    "created_at": f"{t.created_at.isoformat()}Z",
                    "student_name": students.get(t.user_id).name if students.get(t.user_id) else t.name,
                    "student_phone": t.phone,
                }
                for t in trials
            ]
        }
    )

@app.get("/api/student/profile")
@login_required(role="student")
def student_profile():
    student = db.session.get(User, session["user_id"])
    if not student:
        return jsonify({"error": "not found"}), 404
    return jsonify({"profile": student.to_public()})


@app.get("/api/student/trials")
@login_required(role="student")
def student_trials():
    student_id = session["user_id"]
    trials = TrialRequest.query.filter_by(user_id=student_id).order_by(TrialRequest.created_at.desc()).all()
    return jsonify(
        {
            "trials": [
                {
                    "id": t.id,
                    "name": t.name,
                    "phone": t.phone,
                    "subject": t.subject,
                    "created_at": f"{t.created_at.isoformat()}Z",
                }
                for t in trials
            ]
        }
    )


@app.get("/api/teacher/profile")
@login_required(role="teacher")
def teacher_profile():
    teacher = db.session.get(User, session["user_id"])
    skills = [s.name for s in TeacherSkill.query.filter_by(teacher_id=teacher.id).all()]
    return jsonify({"profile": teacher.to_public(), "skills": skills})


@app.put("/api/teacher/profile")
@login_required(role="teacher")
def update_teacher_profile():
    payload = request.get_json(silent=True) or {}
    teacher = db.session.get(User, session["user_id"])
    for field in ["name", "subject", "price", "city", "image"]:
        if field in payload:
            setattr(teacher, field, payload[field])
    if "rating" in payload:
        try:
            teacher.rating = float(payload["rating"])
        except (TypeError, ValueError):
            return jsonify({"error": "rating must be a number"}), 400
    db.session.commit()
    return jsonify({"message": "profile_updated", "profile": teacher.to_public()})


@app.post("/api/teacher/skills")
@login_required(role="teacher")
def add_skill():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    if not name:
        return jsonify({"error": "skill name required"}), 400
    teacher_id = session["user_id"]
    existing = TeacherSkill.query.filter_by(teacher_id=teacher_id, name=name).first()
    if existing:
        return jsonify({"message": "skill_exists"})
    db.session.add(TeacherSkill(teacher_id=teacher_id, name=name))
    db.session.commit()
    return jsonify({"message": "skill_added", "skill": name})


@app.delete("/api/teacher/skills")
@login_required(role="teacher")
def remove_skill():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    if not name:
        return jsonify({"error": "skill name required"}), 400
    teacher_id = session["user_id"]
    deleted = TeacherSkill.query.filter_by(teacher_id=teacher_id, name=name).delete()
    db.session.commit()
    if not deleted:
        return jsonify({"error": "skill not found"}), 404
    return jsonify({"message": "skill_removed", "skill": name})


@app.get("/api/teacher/stats")
@login_required(role="teacher")
def teacher_stats():
    total_trials = TrialRequest.query.count()
    return jsonify({"trials": total_trials})


@app.get("/reset/<token>")
def reset_page(token):
    file_path = FRONTEND_DIR / "reset.html"
    if file_path.exists():
        return send_from_directory(FRONTEND_DIR, "reset.html")
    return jsonify({"error": "reset page not found"}), 404


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_frontend(path):
    file_path = FRONTEND_DIR / path
    if file_path.exists() and file_path.is_file():
        return send_from_directory(FRONTEND_DIR, path)
    return jsonify({"error": "not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
