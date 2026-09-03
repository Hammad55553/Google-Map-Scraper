# Lead Generation & Job Hunt Automation System

## Project Overview
This project is a full-stack automation tool built with a **Next.js frontend** and a **FastAPI backend**. It has two main modes of operation:
1. **Lead Generation**: Scrapes Google Maps for B2B businesses, extracts verified emails, and automatically sends personalized cold-email pitches.
2. **Job Hunt**: Scrapes tech/software companies, extracts their HR/Contact emails, and automatically sends tailored job applications (including a dynamically generated ATS-optimized PDF resume).

---

## Architecture
- **Frontend**: Next.js (React), TailwindCSS.
- **Backend**: FastAPI (Python), Playwright (for async headless browser scraping), `fpdf2` (for dynamic PDF generation).
- **Communication**: Frontend communicates with backend via REST APIs (e.g., `/api/jobs/scrape`, `/api/jobs/apply`).
- **Database**: SQLite with SQLAlchemy (for saving leads, managing sent emails, avoiding duplicates).

---

## Key Features & Logic

### 1. The Scraper (`scraper.py` & `job_scraper.py`)
- Uses **Playwright** to scrape Google Maps data (Name, Address, Phone, Website).
- **Social Media Bypass**: Explicitly ignores social media domains (Facebook, Instagram, LinkedIn, etc.) to prevent getting stuck or extracting fake emails.
- **2-Method Email Extraction**: 
  1. Scans the company's website (and `/contact`, `/about` pages) for `mailto:` tags and regex patterns.
  2. Fallback: If no email is found but a domain exists, guesses `info@domain.com`.
- **Address Cleanup**: Automatically removes Google Map icon unicode characters (``).
- **Duplicate Prevention**: Keeps track of emails sent to avoid spamming the same company twice.

### 2. Job Hunt Module
- **Custom Search Grid**: Exact replica of the Leads tab (Country, State/City, Category, Radius).
- **Dynamic Pitch Generator**: The pitch (`job_pitch_generator.py`) automatically tailors itself by inserting the `[Company Name]` and randomizes the user's experience between `3.5+` and `4+` years to add human-like variation.
- **ATS-Optimized Resume Generator (`resume_generator.py`)**: 
  - Instead of requiring a LaTeX compiler, the system uses `fpdf2` to dynamically generate a PDF that *visually identically mimics* a professional ATS-optimized LaTeX layout.
  - Automatically appends the target company's name to the Professional Summary (e.g., *"seeking to deliver high-quality products at [Company Name]"*).
  - Includes clickable GitHub and LinkedIn links.
- **Custom Resume Upload**: Users can optionally upload their own custom PDF resume via the UI (`/api/jobs/resume/upload`), which the system will use instead of the auto-generated one.

### 3. Email Sending (`index.py`)
- Uses Python's `smtplib` (SMTP over Gmail).
- Converts Markdown-style bold text (e.g., `*text*`) to HTML `<b>text</b>` for professional formatting.
- Attaches the PDF CV (either custom uploaded or auto-generated) as a `MIMEBase` attachment.

---

## AI Agent Handover Notes (If you are another AI reading this)
- **Do not break the Scraper**: The scraping logic handles specific edge cases (like the `info@` fallback and skipping `.png/.jpg` emails). Ensure `clean_emails()` is kept intact.
- **Rules of Hooks**: The frontend `page.tsx` was carefully structured to avoid React Hook order mismatch errors. All `useEffect` hooks must remain at the top level before any conditional returns.
- **Resume Generator**: The PDF is generated natively using `fpdf2` in `resume_generator.py` to mimic LaTeX. If the user asks for layout changes, modify the `fpdf2` cell positioning, do NOT try to install or run `pdflatex`.
- **Environment**: Ensure the Python virtual environment (`venv`) is activated before running backend processes. `python-multipart` is installed for handling file uploads.

## How to Run Locally
1. **Backend**:
   ```bash
   cd frontend/api
   source venv/bin/activate
   uvicorn index:app --reload --port 8000
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
