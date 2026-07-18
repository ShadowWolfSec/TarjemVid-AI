# gui.py
import os

def load_html():
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "structure.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    with open(os.path.join(base_dir, "styles.css"), "r", encoding="utf-8") as f:
        css_content = f.read()
    with open(os.path.join(base_dir, "scripts.js"), "r", encoding="utf-8") as f:
        js_content = f.read()
    html_content = html_content.replace('<link rel="stylesheet" href="styles.css">', f'<style>{css_content}</style>')
    html_content = html_content.replace('<script src="scripts.js"></script>', f'<script>{js_content}</script>')
    return html_content

# للحفاظ على التوافقية مع main.py القديم
HTML = load_html()