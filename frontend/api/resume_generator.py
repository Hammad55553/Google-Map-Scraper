from fpdf import FPDF
import io

def safe(text):
    """Replace special unicode chars that latin-1 can't handle"""
    if not text: return ""
    return (text
        .replace('\u2013', '-').replace('\u2014', '-')
        .replace('\u2018', "'").replace('\u2019', "'")
        .replace('\u201c', '"').replace('\u201d', '"')
        .replace('\u2022', '*').replace('\u00a0', ' ')
        .replace('\u2026', '...')
        .encode('latin-1', 'replace').decode('latin-1')
    )

class ATSResumePDF(FPDF):
    def __init__(self):
        super().__init__(unit='mm', format='letter')
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_margins(15, 15, 15)
        
    def add_header(self):
        # Name
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, safe("Hammad Aslam"), ln=1, align="C")
        
        # Title
        self.set_font("Helvetica", "", 12)
        self.cell(0, 6, safe("React Native & Full-Stack Developer"), ln=1, align="C")
        
        # Contact Info
        self.set_font("Helvetica", "", 10)
        self.cell(0, 5, safe("+92 303 6629101 | hammadaslam78612@gmail.com | linkedin.com/in/hammadaslamkamboh | github.com/hammad55553"), ln=1, align="C")
        self.ln(4)

    def add_section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(25, 25, 112) # MidnightBlue-like
        self.cell(0, 6, safe(title.upper()), ln=1)
        # Draw line
        self.set_draw_color(25, 25, 112)
        self.set_line_width(0.4)
        self.line(self.get_x(), self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def add_summary(self, target_company=None):
        import random
        exp = random.choice(["3.5+", "4+"])
        
        self.add_section_title("Professional Summary")
        self.set_font("Helvetica", "", 10)
        
        tailored_text = ""
        if target_company:
            tailored_text = f" Currently seeking to leverage this cross-platform expertise to drive impact and deliver high-quality products at {target_company}."
            
        summary = (
            f"React Native & Full-Stack Developer with {exp} years of experience architecting and shipping "
            "multiple live production apps across the USA, Malaysia, Canada, and Pakistan. Skilled in building modern web interfaces with "
            "React.js and TypeScript, and robust backends using Python and FastAPI. Proficient in WebRTC video calling, Socket.io real-time chat, "
            "and Google Maps API with sub-second latency. Experienced in building cross-platform mobile, web, and Electron desktop apps and in "
            "AI-assisted development using LLM tools to accelerate delivery, with a strong focus on clean Redux-driven architecture, "
            "performance optimization, and seamless multi-platform deployments." + tailored_text
        )
        self.multi_cell(0, 5, safe(summary))
        self.ln(3)

    def add_education(self):
        self.add_section_title("Education")
        self.set_font("Helvetica", "B", 10.5)
        self.cell(140, 5, safe("Superior University"), ln=0)
        self.cell(0, 5, safe("Lahore, Pakistan"), ln=1, align="R")
        
        self.set_font("Helvetica", "I", 10)
        self.cell(140, 5, safe("Bachelor of Computer Science (Major in Software Development)"), ln=0)
        self.cell(0, 5, safe("2020 - 2024"), ln=1, align="R")
        
        self.set_font("Helvetica", "B", 10.5)
        self.cell(140, 5, safe("Superior Group of Colleges"), ln=0)
        self.cell(0, 5, safe("Hasilpur, Pakistan"), ln=1, align="R")
        
        self.set_font("Helvetica", "I", 10)
        self.cell(140, 5, safe("Intermediate in Computer Science (ICS)"), ln=0)
        self.cell(0, 5, safe("2018 - 2020"), ln=1, align="R")
        self.ln(3)

    def add_experience_item(self, title, date, company, location, bullets):
        self.set_font("Helvetica", "B", 10.5)
        self.cell(130, 5, safe(title), ln=0)
        self.cell(0, 5, safe(date), ln=1, align="R")
        
        self.set_font("Helvetica", "I", 10)
        self.cell(130, 5, safe(company), ln=0)
        self.cell(0, 5, safe(location), ln=1, align="R")
        
        self.set_font("Helvetica", "", 10)
        for bullet in bullets:
            self.set_x(18)
            self.multi_cell(0, 4.5, safe(f"• {bullet}"))
        self.ln(2)

    def add_project_item(self, name, tech, links, bullets):
        self.set_font("Helvetica", "B", 10)
        self.cell(130, 5, safe(f"{name} | {tech}"), ln=0)
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 5, safe(links), ln=1, align="R")
        
        self.set_font("Helvetica", "", 10)
        for bullet in bullets:
            self.set_x(18)
            self.multi_cell(0, 4.5, safe(f"• {bullet}"))
        self.ln(1.5)

    def add_skills(self):
        self.add_section_title("Technical Skills")
        skills = [
            ("Languages", "JavaScript, TypeScript, Python, SQL"),
            ("Frameworks", "React Native, React.js, FastAPI, Node.js, Express.js, Flask, Electron"),
            ("State & UI", "Redux, Redux Toolkit, Context API, React Navigation, Reanimated, Material-UI"),
            ("Databases", "PostgreSQL, Supabase, Firebase Firestore, MongoDB, MySQL"),
            ("AI & Tooling", "Cursor, GitHub Copilot, LLM-Assisted Development, Prompt Engineering, OpenAI & Claude API Integration"),
            ("DevOps & Tools", "Git, GitHub, GitLab, Docker, Jira, Postman, Xcode, Android Studio, VS Code, CI/CD Pipelines"),
            ("Practices", "Agile / Scrum, Unit Testing (Jest), Debugging, Code Review, REST API Design"),
            ("Cloud & APIs", "Firebase (Auth, Firestore, FCM, Hosting), Vercel, Google Maps API, RESTful APIs, JazzCash, EasyPaisa, Stripe"),
            ("Real-time", "WebRTC, Socket.io, Firebase Realtime Database"),
            ("Mobile", "iOS & Android Deployment, Play Store, App Store Publishing"),
        ]
        
        for category, value in skills:
            self.set_font("Helvetica", "B", 10)
            self.set_x(18)
            self.cell(35, 5, safe(f"{category}:"), ln=0)
            self.set_font("Helvetica", "", 10)
            self.multi_cell(0, 5, safe(value))
        self.ln(2)

def generate_resume_pdf(target_company=None):
    pdf = ATSResumePDF()
    pdf.add_header()
    pdf.add_summary(target_company)
    pdf.add_education()
    
    # Experience
    pdf.add_section_title("Experience")
    pdf.add_experience_item(
        "Software Engineer", "Jan 2026 - Present",
        "Asper InfoTech", "Hasilpur, Pakistan",
        [
            "Architected a full-stack e-commerce delivery platform with 3 distinct user modules (customers, shop owners, riders) using React.js, React Native, and Redux, streamlining order workflows across all user roles.",
            "Built an Integrated Communication & Management System (ICMS) supporting 50+ concurrent users via a React.js dashboard, WebRTC video/audio calling, and Socket.io group chat.",
            "Engineered FastAPI backend services with async endpoints and PostgreSQL, significantly reducing API response times under high-concurrency real-time workloads.",
            "Integrated AI/LLM tooling (Cursor, Copilot) into the development workflow to accelerate feature delivery while maintaining code quality through rigorous review.",
            "Streamlined the report generation pipeline to produce PDF/Excel exports in under 2 seconds with dynamic visualizations using React Native Chart Kit.",
            "Deployed live rider tracking via Google Maps API with sub-500 ms real-time location updates, improving delivery accuracy for end users."
        ]
    )
    pdf.add_experience_item(
        "React Native App Developer", "Jun 2025 - Dec 2025",
        "Signature Intech", "Lahore, Pakistan",
        [
            "Launched KarayDaar and KarayDaar Agency - an ecosystem of 2 real estate rental apps achieving a 5.0 rating on Play Store, featuring map-based property search, in-app chat, and CRM tools.",
            "Integrated Firebase (Auth, FCM) and RESTful APIs enabling real-time communication across 1,000+ active property listings.",
            "Boosted app performance through advanced caching strategies and UI rendering improvements, noticeably reducing screen load times across Android and iOS."
        ]
    )
    pdf.add_experience_item(
        "Freelance React Native Developer", "Feb 2025 - May 2025",
        "Self-Employed", "Remote",
        [
            "Shipped 3+ cross-platform mobile projects for international clients using React Native, TypeScript, and Firebase, completing all engagements within agreed timelines.",
            "Integrated 20+ RESTful APIs and Redux state management across 5+ e-commerce and service-based client apps, greatly reducing state-related bugs.",
            "Managed end-to-end project delivery for 3 client engagements covering sprint planning, client communication, and Play Store / App Store releases."
        ]
    )
    pdf.add_experience_item(
        "Mobile App Developer", "Dec 2023 - Jan 2025",
        "The Mind Gauge", "Lahore, Pakistan",
        [
            "Shipped multiple cross-platform applications with React Native & TypeScript backed by FastAPI, serving users across 3 international markets.",
            "Integrated real-time data sync via Firestore and push notifications via FCM, reaching 10,000+ active users across multiple platforms.",
            "Implemented secure JWT/OAuth2 authentication and integrated 3 multi-region payment gateways (Stripe, JazzCash, EasyPaisa) for global transaction support.",
            "Achieved noticeably faster load times through lazy loading, memoization, and aggressive asset caching across production applications."
        ]
    )
    pdf.add_experience_item(
        "React Native Developer (Part-Time)", "Jul 2023 - Sep 2024",
        "Asper InfoTech", "Hasilpur, Pakistan",
        [
            "Built and maintained 5+ mobile apps using React Native, Redux, and RESTful APIs, serving users across Pakistan and international markets.",
            "Developed 40+ responsive UI screens with React Navigation, Reanimated, and Material-UI components, improving UI consistency and stability.",
            "Orchestrated CI/CD pipelines for builds and releases, greatly shortening release cycles with seamless Play Store and App Store deployments."
        ]
    )
    
    # Projects
    pdf.add_section_title("Projects")
    pdf.add_project_item(
        "KarayDaar", "React Native, Firebase, Google Maps, REST APIs", "Play Store | App Store",
        [
            "Cross-platform real estate rental app with map-based property search, in-app chat, and secure JazzCash payment gateway integration, achieving a 5.0 Play Store rating.",
            "Engineered a booking system for property viewings with digital payment confirmation for landlord-tenant security.",
            "Integrated Firebase-powered real-time updates and image processing supporting 1,000+ property listings."
        ]
    )
    pdf.add_project_item(
        "KarayDaar Agency", "React Native, Firebase, CRM, Listing Management", "",
        [
            "Dedicated agency platform for managing property listings, lead tracking, and client communication for real estate firms.",
            "Built a CRM-style dashboard enabling agents to monitor property performance metrics and manage inquiries efficiently."
        ]
    )
    pdf.add_project_item(
        "Beatask", "React Native, Firebase, Stripe, Real-time Chat", "",
        [
            "Handyman service booking app for the US market with Firebase authentication, real-time in-app chat, and Stripe payment processing.",
            "Developed booking management and scheduling workflows supporting live service tracking for seamless customer-to-provider experiences."
        ]
    )
    pdf.add_project_item(
        "MNSUAM Smart Agriculture App", "React Native, FastAPI, GPS, Cloud Sync", "Project Link",
        [
            "Commissioned by the Asian Development Bank to collect verified farmer data to expedite loan approvals, covering 500+ farmers in the field.",
            "Incorporated GPS tracking, real-time sync, and cloud analytics ensuring 99% data accuracy during field data collection."
        ]
    )
    pdf.add_project_item(
        "One Dealer - SIM Card Registration", "React Native, Firebase, OCR", "Play Store | App Store",
        [
            "Mission-critical SIM registration platform leveraging OCR for instant MyKad/Passport data extraction for telecom dealers across Malaysia.",
            "Ensured 99% data accuracy during real-time identity verification, significantly reducing manual entry errors."
        ]
    )
    pdf.add_project_item(
        "AI WhatsApp Voice & Text Agent", "WhatsApp Cloud API, Python, LLM (OpenAI)", "",
        [
            "Built an AI-powered WhatsApp agent on the Meta WhatsApp Cloud API that understands both voice notes and text messages and replies automatically using an LLM (ChatGPT/OpenAI), enabling 24/7 hands-free conversations.",
            "Engineered a pipeline that transcribes incoming voice notes to text, processes intent through the LLM, and returns natural, context-aware responses to users in real time."
        ]
    )
    pdf.add_project_item(
        "ICMS - Integrated Communication & Management System", "React Native, React.js, WebRTC, Socket.io", "",
        [
            "Built the React Native mobile app for an Integrated Communication & Management System, integrating REST APIs for authentication, messaging, and user/data management.",
            "Delivered WebRTC audio/video calling and Socket.io real-time group chat, supporting 50+ concurrent users across mobile and a React.js web dashboard."
        ]
    )
    pdf.add_project_item(
        "Medical Store POS System", "React, Electron, React Native, Supabase", "",
        [
            "Developed a cross-platform Point-of-Sale (POS) system for pharmacies with a React web dashboard, Electron desktop app, and React Native mobile app, all powered by a Supabase backend.",
            "Implemented billing, real-time inventory and stock tracking, expiry alerts, and sales reporting to streamline daily medical-store operations."
        ]
    )
    pdf.add_project_item(
        "Restaurant POS System", "React, Electron, React Native, Supabase", "",
        [
            "Built a complete restaurant POS spanning web, Electron desktop, and mobile, enabling order management, table/menu handling, billing, and kitchen order tickets in one connected system.",
            "Leveraged Supabase for real-time data sync across devices, keeping orders, payments, and stock consistent between counter, kitchen, and management."
        ]
    )
    
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_x(15)
    pdf.cell(0, 5, safe("And several other production apps & systems, including offline-first water delivery, kitchen management, and e-commerce solutions across web, mobile, and desktop."), ln=1)
    pdf.ln(3)

    # Skills
    pdf.add_skills()

    return pdf.output(dest='S').encode('latin-1')

if __name__ == "__main__":
    data = generate_resume_pdf(target_company="Google")
    with open("hammad_resume.pdf", "wb") as f:
        f.write(data)
    print(f"Resume generated: {len(data)} bytes")
