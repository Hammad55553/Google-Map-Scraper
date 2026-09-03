from fpdf import FPDF
import io

def safe(text):
    """Replace special unicode chars that latin-1 can't handle"""
    return (text
        .replace('\u2013', '-').replace('\u2014', '-')
        .replace('\u2018', "'").replace('\u2019', "'")
        .replace('\u201c', '"').replace('\u201d', '"')
        .replace('\u2022', '*').replace('\u00a0', ' ')
    )

def generate_resume_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    # Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, safe("Hammad Aslam"), new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, safe("React Native & Full-Stack Developer"), new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, safe("+92 303 6629101  |  hammadaslam78612@gmail.com  |  LinkedIn  |  GitHub"), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(3)

    pdf.set_draw_color(100, 100, 220)
    pdf.set_line_width(0.8)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    def section_title(title):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(50, 50, 180)
        pdf.cell(0, 7, safe(title), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(150, 150, 220)
        pdf.set_line_width(0.3)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(2)
        pdf.set_text_color(30, 30, 30)

    def body_text(text):
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(180, 4.5, safe(text))

    def bullet(text):
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        pdf.set_x(18)
        pdf.multi_cell(177, 4.5, safe(f"* {text}"))

    def job_title(role, company, period):
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(120, 5, safe(role), new_x="RIGHT", new_y="LAST")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, safe(period), new_x="LMARGIN", new_y="NEXT", align="R")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 4.5, safe(company), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    # Professional Summary
    section_title("PROFESSIONAL SUMMARY")
    body_text("React Native & Full-Stack Developer with 3+ years of experience architecting and shipping multiple live production apps across the USA, Malaysia, Canada, and Pakistan. Skilled in building modern web interfaces with React.js and TypeScript, and robust backends using Python and FastAPI. Proficient in WebRTC video calling, Socket.io real-time chat, and Google Maps API with sub-second latency. Experienced in cross-platform mobile, web, and Electron desktop apps and AI-assisted development using LLM tools.")
    pdf.ln(3)

    # Experience
    section_title("EXPERIENCE")

    job_title("Software Engineer", "Asper InfoTech - Hasilpur, Pakistan", "Jan 2026 - Present")
    bullet("Architected a full-stack e-commerce delivery platform with 3 distinct user modules using React.js, React Native, and Redux.")
    bullet("Built an ICMS supporting 50+ concurrent users via React.js dashboard, WebRTC video/audio calling, and Socket.io group chat.")
    bullet("Engineered FastAPI backend services with async endpoints and PostgreSQL, reducing API response times significantly.")
    bullet("Integrated AI/LLM tooling (Cursor, Copilot) to accelerate feature delivery while maintaining code quality.")
    pdf.ln(2)

    job_title("React Native App Developer", "Signature Intech - Lahore, Pakistan", "Jun 2025 - Dec 2025")
    bullet("Launched KarayDaar and KarayDaar Agency - 2 real estate rental apps achieving a 5.0 rating on Play Store.")
    bullet("Integrated Firebase (Auth, FCM) and RESTful APIs enabling real-time communication across 1,000+ active listings.")
    pdf.ln(2)

    job_title("Freelance React Native Developer", "Self-Employed - Remote", "Feb 2025 - May 2025")
    bullet("Shipped 3+ cross-platform mobile projects for international clients using React Native, TypeScript, and Firebase.")
    bullet("Integrated 20+ RESTful APIs and Redux state management across 5+ e-commerce and service-based client apps.")
    pdf.ln(2)

    job_title("Mobile App Developer", "The Mind Gauge - Lahore, Pakistan", "Dec 2023 - Jan 2025")
    bullet("Shipped cross-platform apps with React Native & TypeScript backed by FastAPI, serving 10,000+ active users.")
    bullet("Implemented JWT/OAuth2 authentication and integrated Stripe, JazzCash, and EasyPaisa payment gateways.")
    pdf.ln(3)

    # Projects
    section_title("KEY PROJECTS")
    projects = [
        ("KarayDaar", "React Native, Firebase, Google Maps", "Real estate rental app with map-based search and secure payments - 5.0 Play Store rating."),
        ("ICMS", "React Native, React.js, WebRTC, Socket.io", "Integrated Communication System supporting 50+ concurrent users with video/audio calling and group chat."),
        ("AI WhatsApp Voice & Text Agent", "WhatsApp Cloud API, Python, OpenAI", "AI-powered WhatsApp agent processing voice notes and text messages with LLM-generated responses 24/7."),
        ("Medical & Restaurant POS", "React, Electron, React Native, Supabase", "Cross-platform POS systems with real-time inventory, billing, and reporting across web, desktop, and mobile."),
        ("MNSUAM Smart Agriculture App", "React Native, FastAPI, GPS", "Commissioned by Asian Development Bank - GPS field data collection covering 500+ farmers with 99% accuracy."),
        ("One Dealer SIM Registration (Malaysia)", "React Native, Firebase, OCR", "Mission-critical SIM registration platform with OCR for instant ID data extraction across Malaysian telecom dealers."),
    ]
    for name, tech, desc in projects:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 5, safe(f"{name}  |  {tech}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(18)
        pdf.multi_cell(177, 4.5, safe(f"* {desc}"))
        pdf.ln(1)
    pdf.ln(1)

    # Skills
    section_title("TECHNICAL SKILLS")
    skills = [
        ("Languages", "JavaScript, TypeScript, Python, SQL"),
        ("Frameworks", "React Native, React.js, FastAPI, Node.js, Express.js, Flask, Electron"),
        ("State & UI", "Redux, Redux Toolkit, Context API, React Navigation, Reanimated, Material-UI"),
        ("Databases", "PostgreSQL, Supabase, Firebase Firestore, MongoDB, MySQL"),
        ("AI & Tooling", "Cursor, GitHub Copilot, LLM-Assisted Development, OpenAI & Claude API Integration"),
        ("Cloud & APIs", "Firebase, Vercel, Google Maps API, Stripe, JazzCash, EasyPaisa, RESTful APIs"),
        ("Real-time", "WebRTC, Socket.io, Firebase Realtime Database"),
        ("DevOps", "Git, GitHub, Docker, Jira, CI/CD Pipelines, Play Store & App Store Publishing"),
    ]
    for category, value in skills:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(50, 50, 50)
        pdf.set_x(15)
        pdf.cell(38, 5, safe(f"{category}:"), new_x="RIGHT", new_y="LAST")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 5, safe(value))
    pdf.ln(2)

    # Education
    section_title("EDUCATION")
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 5, safe("Bachelor of Computer Science - Superior University, Lahore  |  2020-2024"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, safe("Intermediate in Computer Science (ICS) - Superior Group of Colleges  |  2018-2020"), new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


if __name__ == "__main__":
    data = generate_resume_pdf()
    with open("hammad_resume.pdf", "wb") as f:
        f.write(data)
    print(f"Resume generated: {len(data)} bytes")
