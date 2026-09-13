# Raj Kumar Das — Personal Portfolio Website & Admin Inbox System

A complete, modern, professional, responsive, and dark-themed personal portfolio website designed for **Raj Kumar Das**, a B.Tech Computer Science Engineering student (Amity University Jharkhand, Batch 2025–2029, 3rd Semester) and aspiring software developer.

Built with **Python (Flask)**, **SQLite**, **HTML5/CSS3/JavaScript**, and **Bootstrap 5** with custom dark glassmorphism styling.

---

## Features Overview

- **Modern Glassmorphic UI**: Charcoal dark theme (`#0a0c10`), neon cyan/indigo glow accents, smooth scrolling, and hover card elevation.
- **Responsive Navigation**: Sticky header with logo, section links, call-to-action button, and mobile hamburger menu.
- **Hero Section**: Dual CTA, social media profile links, and interactive visual Python code terminal widget.
- **About Me**: Academic details, batch/semester cards, interests list, and editable statistics.
- **Categorized Skills**: Dark glassmorphic cards for Programming, Web Development, AI/ML, Tools, and Design.
- **Interactive Projects**: Category filter tabs (`All`, `Web`, `AI/ML`, `Python`) with project cards, technology tags, features list, Live Demo, and GitHub links.
- **Experience & Education Timelines**: Dedicated sections highlighting hackathons (Smart India Hackathon SIH 2026, Team UNCODED, SentinelAI) and degree coursework.
- **Resume Portal**: Configurable resume download and inline PDF viewer links.
- **Real Backend Contact System**: Form with client validation, anti-spam honeypot, rate limiting, and SQLite database persistence.
- **Email Notifications**: Background SMTP integration sending real-time alerts to the admin email when a visitor submits the contact form.
- **Protected Admin Dashboard & Inbox**:
  - Secure login (`/admin/login`) backed by Werkzeug password hashing.
  - Analytics widgets (Total, Unread, Read, Replied message counts).
  - Search & filter messages inbox (`/admin/messages`).
  - View full message modal, toggle read/unread status, reply via `mailto:`, and delete messages with confirmation.

---

## 1. How to Run the Website Locally

### Prerequisites
- Python 3.9+ installed on your system.

### Steps
1. Navigate to the project directory:
   ```bash
   cd C:\Users\User\.gemini\antigravity\scratch\raj_kumar_das_portfolio
   ```

2. (Optional but recommended) Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the Flask application:
   ```bash
   python app.py
   ```

5. Open your web browser and navigate to:
   - **Portfolio Website**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - **Admin Login Portal**: [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)

---

## 2. Dependencies

The application relies on lightweight standard Python packages specified in `requirements.txt`:

```text
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
python-dotenv>=1.0.0
Werkzeug>=3.0.0
```

To install or update them:
```bash
pip install -r requirements.txt
```

---

## 3. Environment Variables Configuration (`.env`)

Create or edit the `.env` file in the root directory (refer to `.env.example`):

```ini
# Application Secret Key
SECRET_KEY=raj_kumar_das_super_secret_portfolio_key_2026

# Default Admin Account Credentials
ADMIN_EMAIL=admin@rajkumardas.dev
ADMIN_PASSWORD=Admin@12345
ADMIN_NAME=Raj Kumar Das

# Resume File / URL
RESUME_URL=/static/resume.pdf

# Email Server (SMTP) Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
NOTIFICATION_RECIPIENT=rajkumar.das@student.amity.edu
```

---

## 4. Admin Account Credentials

On the first launch, `app.py` automatically initializes `database.db` and seeds the admin user using environment variables:

- **Login URL**: [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)
- **Default Email**: `admin@rajkumardas.dev`
- **Default Password**: `Admin@12345`

*Note: You can change the admin email and password anytime in `.env` before initializing the database or by resetting the password in SQLite.*

---

## 5. Configuring Email Notifications

To receive an instant email alert whenever a visitor submits the contact form:
1. Enable 2-Step Verification on your Gmail (or custom SMTP provider).
2. Generate an **App Password**.
3. Update the following settings in your `.env` file:
   ```ini
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_16_char_app_password
   NOTIFICATION_RECIPIENT=rajkumar.das@student.amity.edu
   ```
4. If SMTP credentials are missing, the contact form will still save all messages cleanly to the database without throwing any errors.

---

## 6. Accessing Admin Dashboard & Viewing Messages

1. Go to `/admin/login` in your browser.
2. Sign in with your admin credentials.
3. Upon authentication, you will be redirected to `/admin/dashboard`.
4. To view received contact form submissions:
   - Click **Messages** in the sidebar or **Open Full Inbox** button.
   - Use the **Search bar** to find messages by sender name, email, or subject.
   - Use the filter tabs (**All**, **Unread**, **Read**, **Replied**) to view specific message groups.
   - Click **View** to read the full body text (automatically updates status to `Read`).
   - Click **Reply** to open your default mail client with a pre-filled `mailto:` draft.
   - Click **Delete** to delete messages after confirmation.

---

## 7. How to Add New Projects

All projects are stored cleanly in the `PORTFOLIO_DATA` dictionary inside `app.py`. To add a new project:

1. Open `app.py`.
2. Locate the `"projects"` array in `PORTFOLIO_DATA`.
3. Append a new project object:

```python
{
    "id": 4,
    "title": "My New Awesome Project",
    "category": "Web",  # Web, AI/ML, Python, or Other
    "tech": ["Python", "Flask", "React"],
    "description": "Short summary of what the project does.",
    "features": ["Feature 1", "Feature 2", "Feature 3"],
    "demo_url": "https://live-demo-link.com",
    "github_url": "https://github.com/rajkumardas/my-project",
    "image": "project_image.jpg"
}
```
4. Restart Flask (`python app.py`). The new project will automatically render with category filtering and tech badges!

---

## 8. How to Change Personal Information

To update personal bio, education details, skills, or social links:

1. Open `app.py`.
2. Modify the corresponding fields inside `PORTFOLIO_DATA`:
   - `"personal_info"`: Name, bio, email, GitHub, LinkedIn links.
   - `"skills"`: Programming languages, web frameworks, AI tools.
   - `"stats"`: Semester, project counts, hackathon notes.
   - `"education"`: Degree, batch, university.
3. Save `app.py` and refresh the page.

---

## 9. Deployment Instructions

### Deploying to Render / Railway / PythonAnywhere

1. **GitHub Repository**: Push this code directory to GitHub.
2. **Render Web Service Setup**:
   - Create a new Web Service on [Render](https://render.com).
   - Connect your GitHub repository.
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (add `gunicorn` to `requirements.txt` if deploying on Linux servers).
3. **Environment Variables**: Add `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, etc., in the Render Dashboard Environment tab.
4. **Database Storage**: SQLite works out of the box. For persistent database across server restarts on cloud hosts like Heroku or Render, you can switch `SQLALCHEMY_DATABASE_URI` in `app.py` to PostgreSQL/Supabase with zero changes to your application logic!

---

## Project Folder Structure

```
raj_kumar_das_portfolio/
├── app.py                     # Main Flask Application & DB Models
├── requirements.txt           # Python Dependencies
├── .env                       # Environment Configurations & Secrets
├── .env.example               # Environment Configuration Template
├── database.db                # SQLite Database (Auto-created)
├── README.md                  # Comprehensive Documentation
├── static/
│   ├── css/
│   │   └── style.css          # Dark Glassmorphic Theme & Responsive Styles
│   ├── js/
│   │   ├── main.js            # Frontend Interactivity & AJAX Contact Handler
│   │   └── admin.js           # Admin Dashboard Interactivity & Message Controls
│   └── resume.pdf             # Sample/Configured Resume Document
└── templates/
    ├── index.html             # Public Portfolio Main Page
    ├── admin_login.html       # Admin Portal Authentication
    ├── admin_dashboard.html   # Admin Overview & Statistics
    └── admin_messages.html    # Full Admin Messages Inbox & Action Controls
```

---

© 2026 Raj Kumar Das. All rights reserved.
