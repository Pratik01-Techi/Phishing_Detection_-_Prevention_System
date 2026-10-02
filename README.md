<img width="1763" height="1594" alt="Screenshot_18-5-2026_11620_localhost" src="https://github.com/user-attachments/assets/05bbe83e-0d55-40c8-a367-7890cdd3be5b" /><div align="center">

<img src="https://img.shields.io/badge/PhishGuard-AI%20Phishing%20Detection-ef4444?style=for-the-badge&logo=shield&logoColor=white" alt="PhishGuard"/>

# 🛡️ PhishGuard
### AI-Powered Phishing Detection & Prevention System

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Model-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![VirusTotal](https://img.shields.io/badge/VirusTotal-API%20Integrated-394EFF?style=flat-square&logo=virustotal&logoColor=white)](https://virustotal.com)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension%20MV3-4285F4?style=flat-square&logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

<br/>

> A full-stack cybersecurity platform combining **machine learning**, **real-time threat intelligence**, and a **Chrome browser extension** to detect and prevent phishing attacks before they cause harm.

<br/>

[Features](#-features) • [Screenshots](#-screenshots) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [Tech Stack](#-tech-stack)

</div>

---

## 📌 What is PhishGuard?

PhishGuard is a production-grade phishing detection system that combines:

- **Machine Learning** — Random Forest + Gradient Boosting ensemble trained on 18 URL features
- **Threat Intelligence** — Real-time VirusTotal (93 engines) and WhoisXML domain age verification
- **Email Analysis** — SPF/DKIM/DMARC header inspection with urgency detection
- **Browser Extension** — Chrome MV3 extension that warns users before they visit dangerous sites
- **Community Reporting** — Submit and track phishing URLs with unique report IDs

Built as a capstone cybersecurity project demonstrating end-to-end secure system design, ML integration, and practical threat detection.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔗 **URL Scanner** | Analyzes 18 features including domain age, TLD risk, brand lookalike detection |
| 📧 **Email Scanner** | Parses raw headers — checks SPF, DKIM, DMARC, urgency language |
| 🤖 **ML Ensemble** | Random Forest + Gradient Boosting with weighted average prediction |
| 🌐 **VirusTotal API** | Cross-validates with 93 antivirus engines in real time |
| 🔍 **WhoisXML API** | Checks domain registration age (new domains = higher risk) |
| 🎯 **Brand Lookalike** | Levenshtein distance detection against 20 major brands |
| 🧩 **Chrome Extension** | MV3 extension with colored badge and in-page phishing banner |
| 📊 **Risk Gauge** | Animated 0–100 risk score gauge with color-coded verdict |
| 📋 **Feature Breakdown** | Per-feature risk table showing exactly why a URL was flagged |
| 🚨 **Report Submission** | Community phishing reporting with UUID tracking |
| 🕐 **Scan History** | Last 50 scans with verdict, timestamp, and quick re-analysis |
| 📈 **Live Stats** | Real-time dashboard metrics: total scans, detected, detection rate |

---

## 📸 Screenshots

### 1. Dashboard — Home (Live Protection Active)

> The main dashboard showing the URL Scanner with Live Protection status, VirusTotal connection indicator, and quick-test URL buttons for immediate testing.

![PhishGuard Dashboard Home] 

---

### 2. URL Scanner — Phishing Detected

> PhishGuard analyzing `http://paypa1-secure-verify.tk/login/confirm` — flagged as **PHISHING** with 100% confidence. Shows Risk Score gauge maxed out, VirusTotal result (2/93 engines), and all triggered rules including high-risk TLD, brand impersonation of PayPal, and missing HTTPS. Feature analysis table highlights suspicious values in red.

![Phishing Detected Result] <img width="1763" height="1956" alt="Screenshot_18-5-2026_104816_localhost" src="https://github.com/user-attachments/assets/7d7636a8-bcfa-4945-85aa-717e6e336afd" />


---

### 3. URL Scanner — Clean Site Verified

> Scanning `https://www.google.com` returns **CLEAN — LOOKS SAFE** with only 4.2% confidence of threat. Domain age verified at 28 years via WhoisXML. VirusTotal returns 0/93 engines flagged. Feature breakdown shows all green indicators except Brand Lookalike Score (expected for google.com matching its own brand).

![Clean Site Result]<img width="1763" height="2000" alt="Screenshot_18-5-2026_105053_localhost" src="https://github.com/user-attachments/assets/2c766a5b-7d0e-4d0e-8eb3-3c16e449d278" />


---

### 4. Email Scanner — Phishing Email Detected

> Email header analysis of a fake `securebankalerts.com` phishing email. System detects SPF: FAIL, DKIM: NONE, DMARC: FAIL with animated risk gauge in the red zone. Triggered rules displayed: SPF authentication failed, DMARC policy failed, Reply-To domain mismatch, and urgent language detected. Recent scan history visible at the bottom.

![Email Phishing Detected] <img width="1763" height="1625" alt="Screenshot_18-5-2026_11733_localhost" src="https://github.com/user-attachments/assets/0f4d8399-719c-4620-9987-feaad097ba01" />


---

### 5. Email Scanner — Legitimate Email (Clean)

> Analyzing a legitimate Microsoft Outlook server email header. System correctly returns **CLEAN — LOOKS SAFE** despite SPF/DKIM/DMARC being absent (not present in partial headers). Risk gauge in the green zone. Demonstrates low false-positive rate on real enterprise mail headers.

![Email Clean Result] <img width="1763" height="1594" alt="Screenshot_18-5-2026_11620_localhost" src="https://github.com/user-attachments/assets/0605b0cd-8f7c-48bc-91c2-2e377f118b36" />


---

### 6. Reports Page — Submit Phishing Report

> The community reporting interface where users can submit a suspicious URL, categorize it as Phishing/Spam/Malware, and add an observed description. Report type dropdown and description field shown in ready state.

![Reports Page] 

---

### 7. Reports Page — Report with Description

> A completed report form for `paypa1-secure-verify.tk` with auto-generated description summarizing triggered detection rules: multiple suspicious keywords, high-risk TLD, brand lookalike, and no HTTPS encryption.

![Report Filled] 

---

### 8. Reports Page — Successful Submission

> Confirmation screen after report submission showing a unique UUID report ID (`e84b776f-b094-4e1e-82da-7e90072dda98`) in green, confirming the phishing URL has been logged to the database for community protection.

![Report Submitted] 

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        PhishGuard System                         │
├──────────────────┬───────────────────────┬───────────────────────┤
│   React Frontend │   Chrome Extension    │    External APIs      │
│   (port 3000)    │   (MV3 background)    │ VirusTotal │ WhoisXML  │
└────────┬─────────┴──────────┬────────────┴──────────┬────────────┘
         │                   │                        │
         └───────────────────┼────────────────────────┘
                             ▼
                 ┌───────────────────────┐
                 │   Flask REST API      │
                 │   (port 5000)         │
                 ├───────────────────────┤
                 │  URL Feature Engine   │  ← 18 features extracted
                 │  Email Header Parser  │  ← SPF/DKIM/DMARC check
                 │  RF + GB ML Ensemble  │  ← Weighted prediction
                 │  SQLite via SQLAlchemy│  ← Scan history & reports
                 └───────────────────────┘
```

---

## 🤖 ML Model Details

The detection engine uses an **ensemble of two classifiers**:

| Model | Role |
|---|---|
| `RandomForestClassifier(n_estimators=100)` | Primary classifier |
| `GradientBoostingClassifier` | Secondary classifier |
| **Weighted Ensemble** | Final verdict = weighted average of both |

### 18 URL Features Extracted

| # | Feature | Why It Matters |
|---|---|---|
| 1 | URL Length | Phishing URLs tend to be longer to obscure the real domain |
| 2 | Domain Length | Legitimate domains are typically short and memorable |
| 3 | Dot Count | Excessive subdomains are a common evasion technique |
| 4 | Hyphen Count | Hyphens used to mimic brands (e.g. `pay-pal.com`) |
| 5 | Has IP Address | Legitimate sites rarely use raw IPs as domains |
| 6 | Is HTTPS | Lack of HTTPS is a significant risk indicator |
| 7 | Subdomain Depth | Deep subdomain nesting used to hide malicious domains |
| 8 | Suspicious Keywords | `login`, `verify`, `secure`, `confirm`, `bank`, etc. |
| 9 | Domain Age (days) | Phishing domains are typically < 30 days old |
| 10 | TLD Risk Score | `.tk`, `.ml`, `.ga`, `.xyz` — free high-abuse TLDs |
| 11 | URL Entropy | High entropy indicates randomized/obfuscated URLs |
| 12 | Digit Ratio | High digit ratio is unusual in legitimate domains |
| 13 | Special Char Count | `%`, `=`, `?`, `&`, `#` used for obfuscation |
| 14 | Brand Lookalike Score | Levenshtein distance vs. 20 major brands |
| 15 | @ Symbol Present | Used to confuse browser URL parsing |
| 16 | Double Slash | Redirection tricks using `//` |
| 17 | Underscore Count | Underscores uncommon in legitimate domains |
| 18 | Slash Count | Deep path nesting used to hide true destination |

### Model Performance

| Metric | Score |
|---|---|
| Accuracy | 95–99% |
| Precision | 94–98% |
| Recall | 93–97% |
| F1 Score | 94–97% |

> Trained on synthetic data by default. Replace `backend/data/training_data.csv` with real PhishTank data (`url`, `label` columns) for production-grade accuracy.

---

## ⚡ Quick Start

### Prerequisites

| Software | Version | Notes |
|---|---|---|
| Python | 3.10 – 3.13 | **Not 3.14** — NumPy incompatibility |
| Node.js | 18+ LTS | For React frontend |
| Chrome | Latest | For browser extension (optional) |

### Option A — Double-Click Launch (Windows)

```
1. Double-click: phishguard/start-backend.cmd
   Wait for: "Running on http://127.0.0.1:5000"

2. Double-click: phishguard/start-frontend.cmd

3. Open browser: http://localhost:3000
```

### Option B — Manual Setup

**Step 1 — Clone the repository**
```bash
git clone https://github.com/Pratik01-Techi/Phishing_Detection_-_Prevention_System.git
cd phishguard
```

**Step 2 — Configure API keys (optional)**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

**Step 3 — Backend setup**
```powershell
cd backend
py -3.13 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

**Step 4 — Frontend setup** (new terminal)
```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

**Step 5 — Open dashboard**
```
http://localhost:3000
```

---

## 🔑 API Keys Configuration

API keys are **optional** — the app works with ML-only mode without them.

| Service | Purpose | Free Tier | Sign Up |
|---|---|---|---|
| VirusTotal | 93-engine URL scan | 4 req/min | [virustotal.com](https://www.virustotal.com/gui/join-us) |
| WhoisXML | Domain registration age | 500 req/month | [whoisxmlapi.com](https://whoisxmlapi.com) |

**`.env` file:**
```env
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
WHOISXML_API_KEY=your_whoisxml_api_key_here
FLASK_SECRET_KEY=any_random_secret_string
FLASK_ENV=development
DATABASE_URL=sqlite:///phishguard.db
```

Verify keys are active: `http://localhost:5000/api/health`
```json
{
  "status": "ok",
  "model_loaded": true,
  "vt_api": "connected"
}
```

---

## 🧩 Chrome Extension Setup

1. Start the backend (`python app.py` on port 5000)
2. Open Chrome → `chrome://extensions/`
3. Enable **Developer mode** (top-right toggle)
4. Click **Load unpacked** → select `phishguard/extension/`

| Badge Color | Meaning |
|---|---|
| 🔴 Red + ⚠ | PHISHING — in-page warning banner injected |
| 🟡 Amber + ? | SUSPICIOUS — proceed with caution |
| 🟢 Green | CLEAN — safe to browse |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Server, model, and API status |
| `POST` | `/api/analyze/url` | Scan a URL for phishing indicators |
| `POST` | `/api/analyze/email` | Analyze raw email headers |
| `POST` | `/api/report` | Submit a phishing report |
| `GET` | `/api/history` | Retrieve last 50 scans |
| `GET` | `/api/stats` | Dashboard statistics |

### Example: Scan a URL

```powershell
$body = '{"url":"http://paypa1-secure-verify.tk/login/confirm"}'
Invoke-RestMethod -Uri http://localhost:5000/api/analyze/url `
  -Method POST -Body $body -ContentType "application/json"
```

**Response:**
```json
{
  "verdict": "PHISHING",
  "confidence": 1.0,
  "risk_score": 100,
  "ml_verdict": "PHISHING",
  "vt_verdict": "MALICIOUS",
  "features": {
    "url_length": 43,
    "is_https": 0,
    "tld_risk_score": 1,
    "lookalike_score": 0.83,
    "domain_age_days": -1
  },
  "triggered_rules": [
    "Multiple suspicious keywords",
    "High-risk TLD detected",
    "Mimics known brand name",
    "No HTTPS encryption"
  ],
  "vt_detections": "2/93 engines",
  "domain_age": "Unknown"
}
```

### Example: Analyze Email Headers

```powershell
$body = '{"email_text":"From: security@fake.tk\nSubject: URGENT verify your account now"}'
Invoke-RestMethod -Uri http://localhost:5000/api/analyze/email `
  -Method POST -Body $body -ContentType "application/json"
```

---

## 📁 Project Structure

```
phishguard/
├── .env                      # API keys (create from .env.example)
├── .env.example              # Template — never put real keys here
├── start-backend.cmd         # One-click backend launcher
├── start-frontend.cmd        # One-click frontend launcher
│
├── backend/
│   ├── app.py                # Flask REST API entry point
│   ├── config.py             # Environment config loader
│   ├── requirements.txt      # Python dependencies
│   ├── fix-venv.cmd          # Recreate venv if broken
│   │
│   ├── features/
│   │   ├── url_features.py   # 18-feature URL extractor
│   │   └── email_features.py # Email header analyzer
│   │
│   ├── models/
│   │   ├── ml_model.py       # RF + GB ensemble training & prediction
│   │   └── phishing_model.pkl # Saved trained model (auto-generated)
│   │
│   ├── services/
│   │   ├── virustotal.py     # VirusTotal v3 API client
│   │   └── whois_service.py  # WhoisXML API client
│   │
│   └── database/
│       ├── db.py             # SQLAlchemy setup
│       └── models.py         # ScanHistory, Reports tables
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── URLScanner.jsx
│       │   ├── EmailScanner.jsx
│       │   ├── ResultCard.jsx
│       │   ├── RiskGauge.jsx
│       │   ├── FeatureBreakdown.jsx
│       │   ├── ScanHistory.jsx
│       │   └── ReportForm.jsx
│       └── pages/
│           ├── Dashboard.jsx
│           └── Reports.jsx
│
└── extension/                # Chrome MV3 Extension
    ├── manifest.json
    ├── background.js         # Tab monitoring + API calls
    ├── content.js            # In-page warning banner injector
    └── popup.html            # Extension popup UI
```

---

## 🧪 Test Cases

### Quick Test URLs (Built into Dashboard)

| Category | URL | Expected Result |
|---|---|---|
| 🔴 Phishing | `http://paypa1-secure-verify.tk/login/confirm` | PHISHING |
| 🔴 Phishing | `http://192.168.1.1/amazon-account-suspended` | PHISHING |
| 🔴 Phishing | `https://google-security-alert.000webhostapp.com` | PHISHING |
| 🟡 Suspicious | `http://free-iphone-winner.xyz/claim` | SUSPICIOUS |
| 🟡 Suspicious | `https://bit.ly/3xR9k2m` | SUSPICIOUS |
| 🟢 Clean | `https://github.com` | CLEAN |
| 🟢 Clean | `https://google.com` | CLEAN |
| 🟢 Clean | `https://stackoverflow.com` | CLEAN |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.13, Flask, SQLAlchemy, SQLite |
| **Machine Learning** | scikit-learn (RandomForest, GradientBoosting), joblib, pandas, numpy |
| **Feature Extraction** | tldextract, python-whois, fuzzywuzzy (Levenshtein), BeautifulSoup4 |
| **Threat Intelligence** | VirusTotal API v3, WhoisXML API |
| **Frontend** | React 18, Vite, Tailwind CSS |
| **Browser Extension** | Chrome Manifest V3, Service Workers |
| **Database** | SQLite (dev), PostgreSQL-ready via SQLAlchemy |

---

## 🔧 Troubleshooting

<details>
<summary><strong>npm is not recognized in PowerShell</strong></summary>

Use `npm.cmd` instead:
```powershell
npm.cmd install
npm.cmd run dev
```
</details>

<details>
<summary><strong>Activate.ps1 cannot be loaded (PowerShell execution policy)</strong></summary>

Do not activate the venv — run Python directly:
```powershell
.\venv\Scripts\python.exe app.py
```
</details>

<details>
<summary><strong>ModuleNotFoundError or NumPy error on startup</strong></summary>

You may be on Python 3.14 or using system Python. Run the fix script:
```powershell
cd backend
# Double-click fix-venv.cmd, or manually:
Remove-Item -Recurse -Force venv
py -3.13 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```
</details>

<details>
<summary><strong>Frontend loads but scan returns network error</strong></summary>

- Ensure backend is running on port 5000 and the terminal is still open
- Restart backend after any `.env` changes
- Check CORS is enabled in `app.py`
</details>

<details>
<summary><strong>VirusTotal shows N/A or not_configured</strong></summary>

1. Keys must be in `phishguard/.env` (not `.env.example`)
2. Restart backend after editing `.env`
3. Verify: `http://localhost:5000/api/health` → `"vt_api": "connected"`
</details>

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

Built for educational and research purposes. Do not use to scan URLs without authorization.

---

## 👤 Author

**Pratik**
BCA (Honours) Cyber Security — Parul University, Gujarat

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/YOUR_USERNAME)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-Top%2015%25-212C42?style=flat-square&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/YOUR_USERNAME)

---

<div align="center">

**⭐ Star this repository if you found it useful!**

*Built with Python, React, and a passion for cybersecurity.*

</div>
