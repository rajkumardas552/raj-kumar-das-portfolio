import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps

from flask import (
    Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key_raj_kumar_das_2026')

# Database Configuration
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, default='Raj Kumar Das')
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Unread') # Unread, Read, Replied

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            flash('Please log in to access the admin dashboard.', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Utility: Email Notification Handler
def send_email_notification(contact_name, contact_email, subject, message_body):
    mail_server = os.getenv('MAIL_SERVER')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    notification_recipient = os.getenv('NOTIFICATION_RECIPIENT', os.getenv('ADMIN_EMAIL', 'rajkumardas@example.com'))

    if not mail_server or not mail_username or not mail_password:
        print(f"[LOG] Email notification skipped (SMTP credentials not fully configured). Message saved in DB from: {contact_email}")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = mail_username
        msg['To'] = notification_recipient
        msg['Subject'] = f"New Portfolio Contact: {subject} (from {contact_name})"

        body = f"""You have received a new contact message on your portfolio!

Sender Details:
----------------------------------------
Name: {contact_name}
Email: {contact_email}
Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message Body:
----------------------------------------
{message_body}

----------------------------------------
View and respond to this message in your Admin Inbox.
"""
        msg.attach(MIMEText(body, 'plain'))

        use_tls = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
        server = smtplib.SMTP(mail_server, mail_port)
        if use_tls:
            server.starttls()
        server.login(mail_username, mail_password)
        server.send_message(msg)
        server.quit()
        print(f"[SUCCESS] Email notification sent to {notification_recipient}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email notification: {str(e)}")
        return False

# Database Initialization Helper
def init_db():
    with app.app_context():
        db.create_all()
        # Seed default admin if none exists
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@rajkumardas.dev')
        admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@12345')
        admin_name = os.getenv('ADMIN_NAME', 'Raj Kumar Das')

        existing_admin = AdminUser.query.filter_by(email=admin_email).first()
        if not existing_admin:
            new_admin = AdminUser(email=admin_email, name=admin_name)
            new_admin.set_password(admin_password)
            db.session.add(new_admin)
            db.session.commit()
            print(f"[INIT] Created initial admin account for {admin_email}")

# Automatically initialize database when WSGI boots
with app.app_context():
    init_db()

# Portfolio Structured Data Store (Easy to update and maintain)
PORTFOLIO_DATA = {
    "personal_info": {
        "name": "Raj Kumar Das",
        "title": "B.Tech CSE Student | Developer | AI & ML Enthusiast",
        "short_bio": "I’m a Computer Science Engineering student passionate about building practical software solutions, exploring AI and Machine Learning, and developing modern web applications.",
        "about": "I am currently pursuing my B.Tech in Computer Science and Engineering (CSE Core) at Amity University Jharkhand (2025–2029, 3rd Semester). I have a strong foundation in software engineering principles, web technologies, machine learning concepts, and cybersecurity fundamentals. I actively participate in hackathons, love tackling complex algorithmic challenges, and continuously seek opportunities to convert innovative ideas into production-ready software.",
        "institution": "Amity University Jharkhand",
        "batch": "2025–2029",
        "semester": "3rd Semester",
        "social": {
            "github": "https://github.com/rajkumardas",
            "linkedin": "https://www.linkedin.com/in/raj-kumar-das-b444a127b",
            "facebook": "https://www.facebook.com/share/1EtHNJc7uU/",
            "instagram": "https://instagram.com/rajkumardas",
            "email": "rajkumar.das@student.amity.edu",
            "whatsapp_qr": "images/whatsapp_qr.jpg"
        }
    },
    "stats": [
        {"number": "3rd Sem", "label": "B.Tech CSE Core"},
        {"number": "2025–29", "label": "Academic Batch"},
        {"number": "5+", "label": "Projects Built"},
        {"number": "SIH '26", "label": "Hackathon Experience"}
    ],
    "skills": {
        "Programming": ["C", "C++", "Python", "JavaScript"],
        "Web Development": ["HTML", "CSS", "Bootstrap", "JavaScript", "Flask"],
        "AI / ML": ["Machine Learning", "CNN", "Autoencoder", "VAE", "MNIST", "Data Analysis"],
        "Tools": ["Git", "GitHub", "VS Code", "Google Colab"],
        "Design": ["Responsive UI", "Dashboard Design", "UI/UX Basics"]
    },
    "projects": [
        {
            "id": 1,
            "title": "Smart Canteen",
            "category": "Web",
            "tech": ["HTML", "CSS", "Bootstrap", "JavaScript", "Python", "Flask"],
            "description": "A smart college canteen pre-ordering system that allows students to browse the menu, add food items to cart, place orders and view their order history.",
            "features": ["Student Login & Profiles", "Dynamic Menu & Cart", "Order Tracking ('My Orders')", "Admin Login & Dashboard", "Real-time Order Management"],
            "demo_url": "#",
            "github_url": "https://github.com/rajkumardas/smart-canteen",
            "image": "smart_canteen.jpg"
        },
        {
            "id": 2,
            "title": "SentinelAI",
            "category": "AI/ML",
            "tech": ["Python", "Machine Learning", "XGBoost", "HTML", "CSS", "JavaScript"],
            "description": "An AI-based network security system designed to detect and forecast potential network attacks from network traffic data.",
            "features": ["Network Traffic Analysis (67 features)", "Attack Detection (DDoS, Brute Force, SQLi)", "XGBoost Classification Model", "Interactive Threat Monitoring Dashboard", "Real-time Security Alerts"],
            "demo_url": "#",
            "github_url": "https://github.com/rajkumardas/sentinel-ai",
            "image": "sentinel_ai.jpg"
        },
        {
            "id": 3,
            "title": "MNIST Deep Learning Benchmark",
            "category": "AI/ML",
            "tech": ["Python", "Machine Learning", "CNN", "Autoencoder", "SAE", "VAE"],
            "description": "A comprehensive deep learning project benchmarking CNN, Autoencoder, SAE, and VAE architecture models on the MNIST handwritten digit dataset.",
            "features": ["Comparative Model Performance Evaluation", "Accuracy, F1-Score, Loss Curves", "Reconstruction Analysis for Autoencoders", "Latent Space Visualization for VAE", "PyTorch / TensorFlow Implementation"],
            "demo_url": "#",
            "github_url": "https://github.com/rajkumardas/mnist-deep-learning",
            "image": "mnist_dl.jpg"
        }
    ],
    "experience": [
        {
            "title": "Smart India Hackathon (SIH 2026)",
            "role": "Frontend Dashboard UI Design / Team Member",
            "team": "Team UNCODED",
            "project": "SentinelAI",
            "period": "2026",
            "description": "Designed and developed the interactive frontend threat-monitoring dashboard for SentinelAI. Contributed to presentation visual assets, security metrics layout, and overall pitch to hackathon evaluators."
        }
    ],
    "achievements": [
        {
            "title": "Smart India Hackathon 2026",
            "category": "Hackathon",
            "description": "Participated and showcased SentinelAI network attack detection solution under Team UNCODED."
        },
        {
            "title": "Technical Projects Developer",
            "category": "Development",
            "description": "Built full-stack Python/Flask applications and responsive web dashboards for real-world utilities."
        },
        {
            "title": "Machine Learning Research & Models",
            "category": "AI / ML",
            "description": "Implemented deep learning architectures (CNN, Autoencoders, VAE) with model accuracy evaluation."
        },
        {
            "title": "College Technical Activities",
            "category": "Leadership",
            "description": "Active participant in departmental coding clubs, tech quizzes, and workshop sessions at Amity University."
        }
    ],
    "education": [
        {
            "degree": "B.Tech in Computer Science & Engineering (CSE Core)",
            "institution": "Amity University Jharkhand",
            "period": "2025–2029",
            "status": "Currently studying 3rd Semester",
            "highlights": "Focused on Data Structures, Algorithms, Web Development, Object Oriented Programming in C++/Python, and Machine Learning."
        }
    ],
    "certifications": [
        {
            "id": 1,
            "title": "Gemini Certified Student",
            "issuer": "Google for Education",
            "date": "August 2026",
            "credential_id": "Valid through Aug 2029",
            "description": "Demonstrated knowledge, skills, and competencies needed to utilize Google AI.",
            "image": "images/certificates/cert_gemini_certified.jpg",
            "badge": "Google AI"
        },
        {
            "id": 2,
            "title": "Junior Software Developer (SSC/Q0508)",
            "issuer": "Skill India & IT-ITeS SSC NASSCOM",
            "date": "September 2025",
            "credential_id": "Roll: 51042RS007023",
            "description": "Government aligned Level-4 certification by NSDC & NASSCOM for Junior Software Developer qualification.",
            "image": "images/certificates/cert_skill_india_nasscom.jpg",
            "badge": "Govt. of India / NASSCOM"
        },
        {
            "id": 3,
            "title": "Python Programming Skill Assessment (90.00%)",
            "issuer": "CodeAlpha",
            "date": "August 2026",
            "credential_id": "CODEALPHA-9048B378",
            "description": "Passed Python Skill Assessment with a 90.00% score demonstrating strong practical proficiency.",
            "image": "images/certificates/cert_codealpha_python.jpg",
            "badge": "Verified Assessment"
        },
        {
            "id": 4,
            "title": "SQL Analytics & BI on Databricks",
            "issuer": "Databricks | Simplilearn SkillUP",
            "date": "August 2026",
            "credential_id": "Code: 10557865",
            "description": "Completed online course covering SQL Analytics, BI warehousing, and data queries on Databricks.",
            "image": "images/certificates/cert_databricks_sql.jpg",
            "badge": "Databricks"
        },
        {
            "id": 5,
            "title": "Freshers Party Challenge - Google Ambassador",
            "issuer": "Google Student Ambassador Program",
            "date": "July 2026",
            "credential_id": "GSA-2026",
            "description": "Recognized for creative campus engagement, event planning, and innovative use of Gemini AI.",
            "image": "images/certificates/cert_google_freshers.jpg",
            "badge": "Google Ambassador"
        }
    ]
}

# --- ROUTES ---

@app.route('/')
def index():
    resume_url = os.getenv('RESUME_URL', '/static/resume.pdf')
    return render_template('index.html', data=PORTFOLIO_DATA, resume_url=resume_url)

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        # Check honeypot field for anti-spam
        honeypot = request.form.get('website_url', '').strip()
        if honeypot:
            # Silent rejection of bot submission
            return jsonify({'success': True, 'message': 'Message received.'})

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message_text = request.form.get('message', '').strip()

        # Input Validation
        if not name or not email or not subject or not message_text:
            return jsonify({'success': False, 'message': 'All fields are required. Please check your inputs.'}), 400

        if '@' not in email or '.' not in email:
            return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400

        # Save message to database
        new_msg = Message(
            name=name,
            email=email,
            subject=subject,
            message=message_text,
            status='Unread',
            created_at=datetime.utcnow()
        )
        db.session.add(new_msg)
        db.session.commit()

        # Send email notification asynchronously or via helper
        send_email_notification(name, email, subject, message_text)

        return jsonify({
            'success': True,
            'message': "Thank you for contacting me! Your message has been received. I'll get back to you soon."
        })
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Exception in /api/contact: {str(e)}")
        return jsonify({'success': False, 'message': 'An internal error occurred while saving your message. Please try again.'}), 500

@app.route('/download-resume')
def download_resume():
    resume_url = os.getenv('RESUME_URL', '/static/resume.pdf')
    if resume_url.startswith('/static/'):
        filename = os.path.basename(resume_url)
        static_dir = os.path.join(app.root_path, 'static')
        filepath = os.path.join(static_dir, filename)
        if not os.path.exists(filepath):
            # Fallback inline dummy text generator for local test if pdf absent
            return send_from_directory(static_dir, 'sample_resume.pdf', as_attachment=False) if os.path.exists(os.path.join(static_dir, 'sample_resume.pdf')) else redirect(url_for('index'))
        return send_from_directory(static_dir, filename, as_attachment=False)
    return redirect(resume_url)

# --- ADMIN ROUTES ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        admin = AdminUser.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            session['admin_name'] = admin.name
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))

        flash('Invalid email or password. Please try again.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_messages = Message.query.count()
    unread_messages = Message.query.filter_by(status='Unread').count()
    read_messages = Message.query.filter_by(status='Read').count()
    replied_messages = Message.query.filter_by(status='Replied').count()

    total_projects = len(PORTFOLIO_DATA['projects'])
    total_skills = sum(len(skills_list) for skills_list in PORTFOLIO_DATA['skills'].values())

    recent_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()

    return render_template('admin_dashboard.html',
                           total_messages=total_messages,
                           unread_messages=unread_messages,
                           read_messages=read_messages,
                           replied_messages=replied_messages,
                           total_projects=total_projects,
                           total_skills=total_skills,
                           recent_messages=recent_messages,
                           data=PORTFOLIO_DATA)

@app.route('/admin/messages')
@login_required
def admin_messages():
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '').strip()

    query = Message.query

    if status_filter in ['Unread', 'Read', 'Replied']:
        query = query.filter_by(status=status_filter)

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            (Message.name.like(search_pattern)) |
            (Message.email.like(search_pattern)) |
            (Message.subject.like(search_pattern)) |
            (Message.message.like(search_pattern))
        )

    messages = query.order_by(Message.created_at.desc()).all()

    return render_template('admin_messages.html',
                           messages=messages,
                           current_filter=status_filter,
                           search_query=search_query)

@app.route('/admin/api/messages/<int:msg_id>/status', methods=['POST'])
@login_required
def update_message_status(msg_id):
    msg = db.get_or_404(Message, msg_id)
    new_status = request.json.get('status')
    if new_status in ['Unread', 'Read', 'Replied']:
        msg.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'new_status': msg.status})
    return jsonify({'success': False, 'message': 'Invalid status'}), 400

@app.route('/admin/api/messages/<int:msg_id>/delete', methods=['POST'])
@login_required
def delete_message(msg_id):
    msg = db.get_or_404(Message, msg_id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Message deleted successfully.'})

# --- RUN APP ---
if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
