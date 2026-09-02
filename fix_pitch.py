with open("frontend/api/pitch_generator.py", "r") as f:
    content = f.read()

# Remove asterisks
content = content.replace("*", "")

# Replace em-dash with a comma or standard hyphen
content = content.replace("—", "-")

# Remove long horizontal lines
content = content.replace("------------------------------------", "")

with open("frontend/api/pitch_generator.py", "w") as f:
    f.write(content)
