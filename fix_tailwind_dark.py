with open("frontend/tailwind.config.ts", "r") as f:
    content = f.read()

if "darkMode:" not in content:
    content = content.replace("export default {", "export default {\n  darkMode: 'class',")
    with open("frontend/tailwind.config.ts", "w") as f:
        f.write(content)
