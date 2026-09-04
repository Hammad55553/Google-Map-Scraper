import random

def generate_job_pitch(company_name: str) -> str:
    exp = random.choice(["3.5+", "4+"])
    return f"""Dear Hiring Manager at {company_name},

I hope this email finds you well. I'm Hammad Aslam, a React Native & Full-Stack Developer with {exp} years of experience building and shipping production-grade apps across the USA, Malaysia, Canada, and Pakistan.

I'm writing to express my strong interest in software development opportunities (both remote and on-site) at {company_name}. I believe my background aligns well with modern tech teams building scalable mobile and web products.

🚀 What I Bring to the Table

📱 Mobile (React Native)
Cross-platform iOS & Android apps — from real estate platforms to AI-powered WhatsApp bots, serving 10,000+ active users. 5.0 Play Store rating on live products.

🌐 Web & Backend
React.js frontends with TypeScript + FastAPI/Node.js backends, PostgreSQL/Supabase databases, and real-time systems via WebRTC & Socket.io supporting 50+ concurrent users.

🤖 AI Integration
Hands-on experience integrating OpenAI & Claude APIs, building LLM-powered agents, and using AI tooling (Cursor, Copilot) to accelerate delivery without sacrificing quality.

☁️ Deployment & DevOps
Firebase, Vercel, Docker, CI/CD pipelines, Play Store & App Store publishing — full production lifecycle ownership.

💡 Proven Track Record & Flexibility
I am fully equipped to work both remotely and on-site. I have successfully delivered projects for international clients (USA, Malaysia, Canada), adapting seamlessly to different work environments and time zones with excellent communication.

I have attached my CV for your review. I would love a quick call to discuss how I can contribute to {company_name}'s engineering team.

📱 WhatsApp/Phone: +92 303 6629101
📧 Email: hammadaslam78612@gmail.com
💼 LinkedIn: https://www.linkedin.com/in/hammadaslamkamboh/
💻 GitHub: https://github.com/Hammad55553/

Thank you for your time. I look forward to hearing from you.

Best regards,
Hammad Aslam
React Native & Full-Stack Developer"""
