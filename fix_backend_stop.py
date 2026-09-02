with open("frontend/api/index.py", "r") as f:
    content = f.read()

# Add cancel flag to state
old_state = """scrape_status = {
    "status": "idle",
    "progress": 0,
    "total": 50, # New limit of 50
    "message": ""
}"""
new_state = """scrape_status = {
    "status": "idle",
    "progress": 0,
    "total": 50, # New limit of 50
    "message": "",
    "cancel": False
}"""
content = content.replace(old_state, new_state)

# Add stop endpoint
stop_endpoint = """
@app.post("/api/scrape/stop")
def stop_scraping():
    global scrape_status
    scrape_status["cancel"] = True
    return {"message": "Scraping cancellation requested"}
"""
if "@app.post(\"/api/scrape/stop\")" not in content:
    content = content + stop_endpoint

# Add check inside scraping loop. The scraper loop is actually in scraper.py or inside run_scraper? 
# Wait, index.py calls `run_scraper` from scraper.py OR defines a local `run_scraper` wrapper.
# Let's check how the loop is handled.
# Ah, `scraper.py` handles the main scraping logic.
