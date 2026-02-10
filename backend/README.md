# EduGlow Backend

## Run locally
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

App runs at `http://127.0.0.1:5000` and serves the frontend from the project root.

## Email reset configuration
Set these environment variables in `backend/.env`:
- `EDUGLOW_SMTP_HOST`
- `EDUGLOW_SMTP_PORT` (default: 587)
- `EDUGLOW_SMTP_USER`
- `EDUGLOW_SMTP_PASS`
- `EDUGLOW_SMTP_FROM` (defaults to `EDUGLOW_SMTP_USER`)
- `EDUGLOW_SMTP_TLS` (true/false)
- `EDUGLOW_BASE_URL` (default: `http://127.0.0.1:5000`)
- `EDUGLOW_SECRET_KEY`

## Demo accounts
- Teacher: `teacher@example.com` / `password123`
- Student: `student@example.com` / `password123`
