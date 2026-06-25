# PhishGuard — AI Phishing Detection & Prevention System

PhishGuard is a full-stack security platform that combines machine learning, rule-based analysis, VirusTotal integration, WhoisXML domain lookup, and a Chrome extension to detect and prevent phishing attacks in real time.

---

## Table of Contents

1. [Publishing to GitHub (Public Repo)](#publishing-to-github-public-repo)
2. [Prerequisites](#prerequisites)
3. [Quick Start (Easiest)](#quick-start-easiest)
4. [First-Time Setup](#first-time-setup)
5. [Run the Project (Every Time)](#run-the-project-every-time)
6. [API Keys Configuration](#api-keys-configuration)
7. [Chrome Extension](#chrome-extension)
8. [Verify Everything Works](#verify-everything-works)
9. [API Endpoints & curl Examples](#api-endpoints--curl-examples)
10. [Troubleshooting](#troubleshooting)
11. [Project Structure](#project-structure)
12. [Tech Stack](#tech-stack)

---

## Publishing to GitHub (Public Repo)

The project folder contains **only source files** safe for public upload. Local/generated files have been removed:

| Removed (do not upload) | Recreate after clone |
|-------------------------|----------------------|
| `.env` (API secrets) | `copy .env.example .env` |
| `backend/venv/` | `py -3.13 -m venv venv` + `pip install -r requirements.txt` |
| `frontend/node_modules/` | `npm.cmd install` |
| `backend/phishguard.db` | Auto-created on first run |
| `backend/models/*.pkl` | Auto-trained on first `app.py` run |
| `backend/data/training_data.csv` | Auto-generated on first train |
| `__pycache__/` | Auto-created by Python |

### Files to upload (complete list)

```
phishguard/
├── .env.example
├── .gitignore
├── README.md
├── start-backend.cmd
├── start-backend.ps1
├── start-frontend.cmd
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── fix-venv.cmd
│   ├── data/.gitkeep
│   ├── database/          (db.py, models.py, __init__.py)
│   ├── features/          (url_features.py, email_features.py)
│   ├── models/            (ml_model.py, .gitkeep)
│   └── services/          (virustotal.py, whois_service.py)
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── run-dev.cmd
│   ├── start-dev.cmd
│   └── src/               (all .jsx, .js, .css files)
│
└── extension/
    ├── manifest.json
    ├── background.js
    ├── content.js
    ├── popup.html
    ├── popup.js
    └── icons/             (icon16.png, icon48.png, icon128.png)
```

### Upload commands

```powershell
cd "YOUR_PATH\phishguard"
git init
git add .
git status
git commit -m "Initial commit: PhishGuard AI phishing detection"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/phishguard.git
git push -u origin main
```

Before `git add`, confirm `git status` does **not** list `.env`, `venv/`, or `node_modules/`.

### After cloning (setup on any machine)

```powershell
copy .env.example .env
# Edit .env with your API keys (optional)

cd backend
py -3.13 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py

cd ..\frontend
npm.cmd install
npm.cmd run dev
```

> **Security:** Never commit `.env`. If keys were ever pushed to GitHub, regenerate them on VirusTotal and WhoisXML.

---

## Prerequisites

Install these **once** before running the project:

| Software | Version | Download | Verify |
|----------|---------|----------|--------|
| **Python** | 3.10 – 3.13 (**not 3.14**) | https://www.python.org/downloads/ | `py -0p` |
| **Node.js** | 18+ LTS | https://nodejs.org/ | `node -v` and `npm.cmd -v` |
| **Chrome** | Latest | (optional, for extension) | — |

> **Important:** Use **Python 3.13** for this project. Python 3.14 causes NumPy/scikit-learn errors.

During Python installation, enable **“Add Python to PATH”**.

---

## Quick Start (Easiest)

Use **two separate windows**. Start backend **first**, then frontend.

### Step 1 — Backend

Double-click:

```
phishguard/start-backend.cmd
```

Wait until you see: `Running on http://127.0.0.1:5000`  
**Do not close this window.**

### Step 2 — Frontend

Double-click:

```
phishguard/start-frontend.cmd
```

Or double-click: `phishguard/frontend/run-dev.cmd`

### Step 3 — Open dashboard

Browser: **http://localhost:3000**

---

## First-Time Setup

Run these commands **only the first time** (or after deleting `venv` / `node_modules`).

### 1. API keys (optional but recommended)

```powershell
cd "YOUR_PATH\phishguard"
copy .env.example .env
```

Edit `phishguard\.env` and paste your real keys (see [API Keys Configuration](#api-keys-configuration)).

> **Never** put real API keys in `.env.example` — only in `.env`.

### 2. Backend setup

```powershell
cd "YOUR_PATH\phishguard\backend"

# Create virtual environment with Python 3.13
py -3.13 -m venv venv

# Install dependencies
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

On first `app.py` run, the ML model trains automatically (~10–30 seconds) and saves to `backend/models/phishing_model.pkl`.

### 3. Frontend setup

**PowerShell:**

```powershell
cd "YOUR_PATH\phishguard\frontend"
npm.cmd install
```

**Command Prompt (cmd):**

```cmd
cd /d "YOUR_PATH\phishguard\frontend"
npm install
```

Replace `YOUR_PATH` with your actual folder path, for example:

```
c:\Users\Pratik\OneDrive\Desktop\Phishing Detection & Prevention System\phishguard
```

---

## Run the Project (Every Time)

You need **2 terminals**. Backend must run **before** frontend.

### Terminal 1 — Backend (Flask API)

**PowerShell:**

```powershell
cd "YOUR_PATH\phishguard\backend"
.\venv\Scripts\python.exe app.py
```

**Command Prompt:**

```cmd
cd /d "YOUR_PATH\phishguard\backend"
venv\Scripts\python.exe app.py
```

| Item | Value |
|------|--------|
| API URL | http://localhost:5000 |
| Health check | http://localhost:5000/api/health |

Keep this terminal **open**.

---

### Terminal 2 — Frontend (React dashboard)

**PowerShell** (use `npm.cmd` — avoids script policy errors):

```powershell
cd "YOUR_PATH\phishguard\frontend"
npm.cmd run dev
```

**Alternative if npm fails in PowerShell:**

```powershell
cd "YOUR_PATH\phishguard\frontend"
node .\node_modules\vite\bin\vite.js
```

**Command Prompt:**

```cmd
cd /d "YOUR_PATH\phishguard\frontend"
npm run dev
```

| Item | Value |
|------|--------|
| Dashboard URL | http://localhost:3000 |

---

### Run order summary

```
1. Backend  →  http://localhost:5000   (Terminal 1)
2. Frontend →  http://localhost:3000   (Terminal 2)
3. Browser  →  Open dashboard and scan URLs
```

---

## API Keys Configuration

API keys are **optional**. Without them, the app uses ML + rules only.

| Service | Purpose | Sign up |
|---------|---------|---------|
| **VirusTotal** | Multi-engine URL scan (`45/72 engines`) | https://www.virustotal.com/gui/join-us |
| **WhoisXML** | Domain registration age | https://whoisxmlapi.com |

### Where to paste keys

| File | Use |
|------|-----|
| `phishguard\.env` | **Paste real keys here** (local only — **not uploaded to GitHub**) |
| `phishguard\.env.example` | Template only — placeholders, safe for public repo |

Create `.env` locally (not included in the public repository):

```powershell
copy .env.example .env
```

### Example `.env` file

Create `phishguard\.env`:

```env
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
WHOISXML_API_KEY=your_whoisxml_api_key_here
FLASK_SECRET_KEY=any_random_secret_string
FLASK_ENV=development
DATABASE_URL=sqlite:///phishguard.db
```

### After adding or changing keys

1. **Stop** the backend (Ctrl+C)
2. **Start** again: `.\venv\Scripts\python.exe app.py`
3. Check: http://localhost:5000/api/health  
   - `"vt_api": "connected"` → VirusTotal is working  
   - `"vt_api": "not_configured"` → key missing or backend not restarted

---

## Chrome Extension

1. Start the **backend** first (`python app.py` on port 5000)
2. Open Chrome → `chrome://extensions/`
3. Enable **Developer mode** (top right)
4. Click **Load unpacked**
5. Select folder: `phishguard/extension`

| Badge | Meaning |
|-------|---------|
| Red + ⚠ | PHISHING |
| Amber + ? | SUSPICIOUS |
| Green | CLEAN |

Phishing sites show a red warning banner at the top of the page.

---

## Verify Everything Works

### Backend health

**PowerShell:**

```powershell
Invoke-RestMethod http://localhost:5000/api/health
```

**Browser:** http://localhost:5000/api/health

Expected response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "vt_api": "connected"
}
```

### Test URL scan (dashboard)

| Type | Test URL |
|------|----------|
| Phishing | `http://paypa1-secure-verify.tk/login/confirm` |
| Clean | `https://github.com` |

### Quick test buttons

The dashboard includes **Quick Test** buttons for phishing, suspicious, and clean URLs.

---

## API Endpoints & curl Examples

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server & model status |
| POST | `/api/analyze/url` | Scan a URL |
| POST | `/api/analyze/email` | Scan email content |
| POST | `/api/report` | Submit phishing report |
| GET | `/api/history` | Last 50 scans |
| GET | `/api/stats` | Dashboard statistics |

**PowerShell examples:**

```powershell
# Health
Invoke-RestMethod http://localhost:5000/api/health

# Analyze URL
$body = '{"url":"http://paypa1-secure-verify.tk/login/confirm"}'
Invoke-RestMethod -Uri http://localhost:5000/api/analyze/url -Method POST -Body $body -ContentType "application/json"

# Analyze email
$body = '{"email_text":"From: security@fake.tk`nSubject: URGENT verify your account now"}'
Invoke-RestMethod -Uri http://localhost:5000/api/analyze/email -Method POST -Body $body -ContentType "application/json"

# History
Invoke-RestMethod http://localhost:5000/api/history

# Stats
Invoke-RestMethod http://localhost:5000/api/stats
```

---

## Troubleshooting

### `'npm' is not recognized` or PowerShell blocks npm

Use **Command Prompt** instead, or in PowerShell:

```powershell
npm.cmd install
npm.cmd run dev
```

Or run Vite directly:

```powershell
node .\node_modules\vite\bin\vite.js
```

---

### `Activate.ps1 cannot be loaded` (PowerShell)

**Do not activate venv.** Run Python from venv directly:

```powershell
.\venv\Scripts\python.exe app.py
```

---

### `ModuleNotFoundError: No module named 'dotenv'` or NumPy error

You are using **system Python** instead of venv, or **Python 3.14**.

**Fix:**

```powershell
cd "YOUR_PATH\phishguard\backend"
```

Double-click **`fix-venv.cmd`**, or run manually:

```powershell
Remove-Item -Recurse -Force venv
py -3.13 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

---

### `'Prevention' is not recognized` (frontend / Vite)

Caused by **spaces in the folder path**. Use:

```powershell
npm.cmd run dev
```

or:

```powershell
node .\node_modules\vite\bin\vite.js
```

Or move the project to a path without spaces, e.g. `C:\Projects\phishguard`.

---

### Frontend loads but scan fails / network error

- Backend must be running on port **5000**
- Keep the backend terminal open
- Restart backend after changing `.env`

---

### VirusTotal shows `N/A` or `vt_api: not_configured`

1. Keys must be in `phishguard\.env` (not `.env.example`)
2. Restart backend after editing `.env`
3. Check health endpoint for `"vt_api": "connected"`

---

### Port 5000 already in use

Close other terminals running `app.py`, or stop the old process in Task Manager.

---

## Project Structure

```
phishguard/
├── .env.example            # Template only (copy to .env locally)
├── .gitignore              # Excludes secrets & generated files
├── start-backend.cmd       # Double-click to run API
├── start-frontend.cmd      # Double-click to run dashboard
├── README.md
│
├── backend/
│   ├── app.py              # Flask REST API entry point
│   ├── config.py
│   ├── requirements.txt
│   ├── fix-venv.cmd        # Recreate venv with Python 3.13
│   ├── data/               # training_data.csv (generated, gitignored)
│   ├── features/           # URL & email feature extraction
│   ├── models/             # ML code (.pkl generated locally, gitignored)
│   ├── services/           # VirusTotal, WhoisXML
│   └── database/           # SQLite models
│
├── frontend/
│   ├── package.json
│   ├── run-dev.cmd         # Alternative frontend launcher
│   └── src/                # React components & pages
│
└── extension/              # Chrome MV3 extension
    ├── manifest.json
    ├── background.js
    ├── content.js
    └── popup.html

# NOT in repo (local only): .env, backend/venv/, frontend/node_modules/,
# backend/phishguard.db, backend/models/phishing_model.pkl
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PhishGuard System                        │
├──────────────┬──────────────────────┬───────────────────────────┤
│   React UI   │   Chrome Extension   │      External APIs        │
│  (port 3000) │   (MV3 background)   │  VirusTotal | WhoisXML    │
└──────┬───────┴──────────┬───────────┴─────────────┬─────────────┘
       │                  │                         │
       └──────────────────┼─────────────────────────┘
                          ▼
              ┌───────────────────────┐
              │   Flask REST API      │
              │   (port 5000)         │
              ├───────────────────────┤
              │ URL Features (18)     │
              │ Email Analyzer        │
              │ RF + GB Ensemble ML   │
              │ SQLite (SQLAlchemy)   │
              └───────────────────────┘
```

---

## Model Accuracy

Trained on synthetic data by default on first run. Metrics with real PhishTank/UCSD CSV (`backend/data/training_data.csv`, columns: `url`, `label`):

| Metric | Typical range |
|--------|----------------|
| Accuracy | 95–99% |
| Precision | 94–98% |
| Recall | 93–97% |
| F1 Score | 94–97% |

---

## Tech Stack

| Layer | Technologies |
|-------|----------------|
| Backend | Python, Flask, scikit-learn, SQLAlchemy, SQLite |
| Frontend | React, Vite, Tailwind CSS |
| Extension | Chrome Manifest V3 |
| APIs | VirusTotal v3, WhoisXML (optional) |
| Libraries | tldextract, python-whois, fuzzywuzzy, pandas, numpy, joblib, BeautifulSoup |

---

## License

MIT — for educational and research purposes.
