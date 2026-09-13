import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_resume_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), 'static', 'resume.pdf')
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor('#1e293b')    # Deep Slate/Navy
    ACCENT = colors.HexColor('#0284c7')     # Vibrant Blue/Cyan
    DARK_TEXT = colors.HexColor('#0f172a')  # Dark charcoal text
    MUTED_TEXT = colors.HexColor('#475569') # Secondary text

    # Styles
    title_style = ParagraphStyle(
        'NameTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=ACCENT
    )

    contact_style = ParagraphStyle(
        'ContactText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=MUTED_TEXT
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=PRIMARY,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        leftIndent=12
    )

    story = []

    # --- HEADER SECTION ---
    story.append(Paragraph("RAJ KUMAR DAS", title_style))
    story.append(Paragraph("B.Tech Computer Science & Engineering (3rd Sem) | Software & AI Developer", subtitle_style))
    story.append(Spacer(1, 4))
    
    contact_line = "Email: rajkumar.das@student.amity.edu | Location: Ranchi, Jharkhand, India<br/>" \
                   "LinkedIn: linkedin.com/in/raj-kumar-das-b444a127b | GitHub: github.com/rajkumardas"
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=8))

    # --- SUMMARY ---
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = "Enthusiastic Computer Science Engineering student passionate about software development, artificial intelligence, machine learning, and web engineering. Proven ability to construct full-stack Python/Flask applications, machine learning threat detection dashboards (SentinelAI for SIH 2026), and deep learning model benchmarks. Continuous learner with strong algorithmic problem-solving capabilities."
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 8))

    # --- EDUCATION ---
    story.append(Paragraph("EDUCATION", section_heading))
    edu_data = [
        [Paragraph("<b>B.Tech in Computer Science & Engineering (CSE Core)</b>", bold_body), Paragraph("<b>2025 – 2029</b>", ParagraphStyle('R', parent=bold_body, alignment=2))],
        [Paragraph("Amity University Jharkhand — Currently studying 3rd Semester", body_style), Paragraph("Ranchi, India", ParagraphStyle('R2', parent=contact_style, alignment=2))]
    ]
    t_edu = Table(edu_data, colWidths=[5.5*inch, 2.0*inch])
    t_edu.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 1)]))
    story.append(t_edu)
    story.append(Spacer(1, 8))

    # --- TECHNICAL SKILLS ---
    story.append(Paragraph("TECHNICAL SKILLS", section_heading))
    skills_data = [
        [Paragraph("<b>Programming Languages:</b>", bold_body), Paragraph("C, C++, Python, JavaScript, SQL, HTML5, CSS3", body_style)],
        [Paragraph("<b>Web Technologies:</b>", bold_body), Paragraph("Flask, Bootstrap 5, REST APIs, Responsive UI/UX", body_style)],
        [Paragraph("<b>AI & Machine Learning:</b>", bold_body), Paragraph("Machine Learning, CNN, Autoencoders, VAE, XGBoost, Data Analysis", body_style)],
        [Paragraph("<b>Tools & Environment:</b>", bold_body), Paragraph("Git, GitHub, VS Code, Google Colab, Databricks SQL", body_style)]
    ]
    t_skills = Table(skills_data, colWidths=[2.2*inch, 5.3*inch])
    t_skills.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 2)]))
    story.append(t_skills)
    story.append(Spacer(1, 8))

    # --- FEATURED PROJECTS ---
    story.append(Paragraph("PROJECTS", section_heading))
    
    # Project 1
    story.append(Paragraph("<b>SentinelAI — Network Security Attack Forecasting & Detection</b>", bold_body))
    story.append(Paragraph("• Built an AI network traffic security model using XGBoost across 67 features to classify DDoS, Brute Force, and SQLi attacks.", bullet_style))
    story.append(Paragraph("• Designed interactive threat-monitoring dashboard using HTML/CSS/JavaScript and Python.", bullet_style))
    story.append(Spacer(1, 4))

    # Project 2
    story.append(Paragraph("<b>Smart Canteen — College Pre-Ordering System</b>", bold_body))
    story.append(Paragraph("• Full-stack Flask web application allowing students to browse food menus, order online, and track order status.", bullet_style))
    story.append(Paragraph("• Includes student profile auth, order history, and an administrative order management dashboard.", bullet_style))
    story.append(Spacer(1, 4))

    # Project 3
    story.append(Paragraph("<b>MNIST Deep Learning Architecture Benchmark</b>", bold_body))
    story.append(Paragraph("• Implemented CNN, Autoencoder, SAE, and VAE neural network architectures for digit recognition and reconstruction.", bullet_style))
    story.append(Paragraph("• Conducted comparative model accuracy, F1-score, and loss visual analysis.", bullet_style))
    story.append(Spacer(1, 8))

    # --- EXPERIENCE & HACKATHONS ---
    story.append(Paragraph("HACKATHONS & EXPERIENCE", section_heading))
    hack_data = [
        [Paragraph("<b>Smart India Hackathon (SIH 2026) — Team UNCODED</b>", bold_body), Paragraph("<b>2026</b>", ParagraphStyle('R3', parent=bold_body, alignment=2))],
        [Paragraph("Frontend Dashboard UI Designer & Technical Contributor for SentinelAI project.", body_style), Paragraph("", body_style)]
    ]
    t_hack = Table(hack_data, colWidths=[6.0*inch, 1.5*inch])
    t_hack.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 1)]))
    story.append(t_hack)
    story.append(Spacer(1, 8))

    # --- CERTIFICATIONS ---
    story.append(Paragraph("CERTIFICATIONS & ACCREDITATIONS", section_heading))
    story.append(Paragraph("• <b>Gemini Certified Student</b> — Google for Education (Valid through Aug 2029)", bullet_style))
    story.append(Paragraph("• <b>Junior Software Developer (SSC/Q0508)</b> — Skill India & IT-ITeS SSC NASSCOM (Level 4 Govt. Qualification)", bullet_style))
    story.append(Paragraph("• <b>Python Programming Skill Assessment (90.00%)</b> — CodeAlpha (ID: CODEALPHA-9048B378)", bullet_style))
    story.append(Paragraph("• <b>SQL Analytics & BI on Databricks</b> — Databricks | Simplilearn SkillUP (Code: 10557865)", bullet_style))
    story.append(Paragraph("• <b>Google Student Ambassador</b> — Freshers' Party Challenge (Google Student Ambassador Program)", bullet_style))

    doc.build(story)
    print(f"Generated professional PDF resume at: {pdf_path}")

if __name__ == '__main__':
    create_resume_pdf()
