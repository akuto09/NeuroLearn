# NeuroLearn

**AI-Driven Neuroadaptive Learning Platform** — a full-stack prototype (Flask backend + server-rendered frontend) implementing the architecture described in the NeuroLearn PRD and Blueprint: public marketing site, role-based auth (student / teacher / admin), student learning portal, teacher cohort tools, admin panel, and a simulated EEG-based AI engine.

Dark navy/black UI with a cyan "synapse" accent and violet "AI" accent, built around a signature animated EEG waveform motif.

## Quick start

```bash
cd NeuroLearn
pip install -r requirements.txt
python app.py
```

Visit **http://localhost:5000**. A SQLite database (`database/neurolearn.db`) is created and seeded automatically on first run.

### Demo accounts (seeded automatically)

| Role    | Email                  | Password    |
|---------|-------------------------|-------------|
| Admin   | admin@neurolearn.ai     | admin123    |
| Teacher | teacher@neurolearn.ai   | teacher123  |
| Student | student@neurolearn.ai   | student123  |

You can also register new student/teacher accounts from `/register`.

## What's implemented

- **Public site** — home, about, features, courses, pricing, FAQ, contact (with working DB-backed contact form).
- **Authentication** — register, role-aware login, forgot-password flow, logout. Passwords hashed with Werkzeug.
- **Student portal** — dashboard with a live-polling cognitive-state panel (attention / meditation / cognitive load / fatigue), courses, assignments, tests, progress analytics, an AI study assistant chat, and settings.
- **Teacher portal** — cohort dashboard, flagged/at-risk students, roster, assigned courses.
- **Admin panel** — platform stats, user management, course catalog, reports, AI engine threshold configuration.
- **AI engine** (`ai_engine/`) — `eeg_processing.py` simulates a live EEG/behavioral signal stream per user session; `recommendation_engine.py` is a rule-based decision layer that turns those signals into a cognitive-readiness status, an adaptive-learning recommendation, and conversational assistant replies. Exposed via `/api/ai/metrics` and `/api/ai/assistant`.
- **Role-based access control** via `middleware/authentication.py` decorators (`login_required`, `role_required`).
- **Error pages** — custom 403 / 404 / 500.

## Connecting real EEG hardware

`ai_engine/eeg_processing.py` currently generates smooth pseudo-live values so the full product loop (sense → interpret → adapt) can be demonstrated without hardware. To connect a real device:

1. Replace `read_mental_state()` with a reader for your headset's SDK (NeuroSky, Muse, Emotiv, or a raw EEG signal-processing pipeline computing band powers).
2. Keep the same return shape: `{"attention": 0-100, "meditation": 0-100, "cognitive_load": 0-100, "fatigue": 0-100}`.
3. Everything downstream (`recommendation_engine.py`, the dashboard, the assistant) will work unchanged.

## Project structure

```
NeuroLearn/
├── app.py                     # App factory, blueprint registration, error handlers
├── config.py
├── requirements.txt
├── ai_engine/
│   ├── eeg_processing.py      # Simulated EEG/mental-state signal source
│   └── recommendation_engine.py  # Rule-based adaptive engine + assistant replies
├── database/
│   ├── connection.py
│   └── schema.py              # Table definitions + demo seed data
├── middleware/
│   └── authentication.py      # login_required / role_required decorators
├── routes/
│   ├── public_routes.py
│   ├── auth_routes.py
│   ├── student_routes.py
│   ├── teacher_routes.py
│   ├── admin_routes.py
│   └── api_routes.py          # /api/ai/metrics, /api/ai/assistant
├── templates/
│   ├── layouts/                # base.html (public), app_base.html (dashboards)
│   ├── public/ authentication/ student/ teacher/ admin/ errors/
└── static/
    ├── css/style.css           # Design tokens + full stylesheet
    └── js/                     # eeg-wave.js, student/dashboard.js, ai/assistant.js
```

## Notes

- This is a self-contained prototype: SQLite, in-memory simulated EEG state, and rule-based AI. Swap in a real EEG pipeline and a trained model behind the same interfaces to move toward production.
- Sessions use Flask's signed cookie session — set a real `SECRET_KEY` environment variable before any real deployment.
