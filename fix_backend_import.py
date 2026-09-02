with open("frontend/api/index.py", "r") as f:
    content = f.read()

import_code = """
from fastapi import UploadFile, File
import pandas as pd
import io

@app.post("/api/import")
async def import_leads_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        
        # Check if it's an excel file or csv
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')
            
        # Clear existing leads
        db.query(Lead).delete()
        
        for _, row in df.iterrows():
            def get_val(col_name, default=""):
                val = row.get(col_name)
                if pd.isna(val):
                    return default
                return str(val).strip()

            phone_val = get_val("Phone")
            if phone_val.startswith("'"):
                phone_val = phone_val[1:]
                
            lead = Lead(
                place_id=str(uuid.uuid4()),
                business_name=get_val("Business Name"),
                category=get_val("Category"),
                city=get_val("City"),
                rating=float(get_val("Rating", 0)),
                reviews_count=int(float(get_val("Reviews Count", 0))),
                phone=phone_val,
                whatsapp_link=get_val("WhatsApp Link"),
                has_website=bool(get_val("Website")),
                website=get_val("Website"),
                email=get_val("Email"),
                address=get_val("Address"),
                map_url=get_val("Map URL"),
                lead_score=int(float(get_val("Lead Score", 0))),
                lead_grade=get_val("Lead Grade"),
                status=get_val("Status"),
                recommended_pitch=get_val("Recommended Pitch")
            )
            db.add(lead)
            
        db.commit()
        return {"message": f"Successfully imported {len(df)} leads"}
        
    except Exception as e:
        return {"error": str(e)}

"""

if "@app.post(\"/api/import\")" not in content:
    content = content + "\n" + import_code

with open("frontend/api/index.py", "w") as f:
    f.write(content)
