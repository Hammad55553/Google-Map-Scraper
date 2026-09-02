with open("frontend/api/pitch_generator.py", "r") as f:
    content = f.read()

# Replace long dashes
content = content.replace("------------------------------------", "")

# Fix any weird em-dashes
content = content.replace("—", "-")

with open("frontend/api/pitch_generator.py", "w") as f:
    f.write(content)
