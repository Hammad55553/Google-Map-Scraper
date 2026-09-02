with open("frontend/api/index.py", "r") as f:
    content = f.read()

old_status = """    def run_scraper():
        global scrape_status
        scrape_status["status"] = "running"
        
        db = SessionLocal()"""
new_status = """    def run_scraper():
        global scrape_status
        scrape_status["status"] = "running"
        scrape_status["cancel"] = False
        
        db = SessionLocal()"""

content = content.replace(old_status, new_status)

with open("frontend/api/index.py", "w") as f:
    f.write(content)
