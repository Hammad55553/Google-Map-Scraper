with open("frontend/api/index.py", "r") as f:
    content = f.read()

old_export = """@app.get("/api/export")
def export_leads():
    db = SessionLocal()
    leads = db.query(Lead).all()
    db.close()
    
    excel_file = generate_excel_from_leads(leads)
    
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Leads_{date_str}.xlsx"
    
    return StreamingResponse("""

new_export = """@app.get("/api/export")
def export_leads():
    db = SessionLocal()
    leads = db.query(Lead).all()
    db.close()
    
    excel_file = generate_excel_from_leads(leads)
    
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    if leads and leads[0].category and leads[0].city:
        cat_clean = leads[0].category.replace(' ', '_').replace('/', '')
        city_clean = leads[0].city.replace(' ', '_').replace('/', '')
        filename = f"{cat_clean}_{city_clean}_{date_str}.xlsx"
    else:
        filename = f"Leads_{date_str}.xlsx"
    
    return StreamingResponse("""

content = content.replace(old_export, new_export)

with open("frontend/api/index.py", "w") as f:
    f.write(content)

