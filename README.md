# Insurance Automation Pipeline (Local MVP)

Local-first Python project for secure browser automation, OTP-assisted login, data extraction, processing, and upload flow.

## 1) Setup

1. Copy `.env.example` to `.env` and fill credentials.
2. Create venv and install dependencies:

```powershell
& "C:\Users\Owner\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

## 2) Run

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

When OTP appears, enter it manually in terminal input.

## 3) Current scope

- Login flow for Noya sandbox URL.
- OTP manual checkpoint (human-in-the-loop).
- Post-login screenshot for debug/audit.

## 4) Next planned modules

- Site-specific extraction worker (downloads + structured parse).
- Transform worker (Pandas/PDF/Excel pipeline).
- Target-site uploader worker with validation and retry logic.
- Job tracking + persistence (SQLite/PostgreSQL).
