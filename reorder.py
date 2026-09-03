import re

with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

table_start = "{/* Companies Table */}"
send_start = "{/* Send Applications (Always Visible Now) */}"
end_marker = "        </div>\n      )}\n\n    </div>"

table_idx = content.find(table_start)
send_idx = content.find(send_start)
end_idx = content.find(end_marker)

if table_idx != -1 and send_idx != -1 and end_idx != -1:
    section_a = content[table_idx:send_idx]
    section_b = content[send_idx:end_idx]
    
    # Rename Section A (now section 3)
    section_a = section_a.replace("2. Companies Found", "3. Lead Database")
    
    # Rename Section B (now section 2)
    section_b = section_b.replace("3. Send Job Applications", "2. Start Email Campaign")
    section_b = section_b.replace("Send Applications (Always Visible Now)", "Start Email Campaign (Always Visible Now)")
    
    # Reconstruct
    new_content = content[:table_idx] + section_b + section_a + content[end_idx:]
    
    with open("frontend/src/app/page.tsx", "w") as f:
        f.write(new_content)
    print("Reordered successfully.")
else:
    print("Could not find markers.")
