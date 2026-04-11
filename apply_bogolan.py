import os
import re

# 1. Update digital-day.css
css_path = r'c:\Users\USER\digital-day-ctf\static\css\digital-day.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('--bg-main: #0d1117;', '--bg-main: #1A1210;')
css = css.replace('--bg-card: #161b22;', '--bg-card: #2B1D16;')
css = css.replace('--primary-neon: #58a6ff;', '--primary-neon: #ffb703;')
css = css.replace('--danger-red: #ff3e3e;', '--danger-red: #d00000;')
css = css.replace('--text-high: #f0f6fc;', '--text-high: #F3EBD3;')
css = css.replace('--text-dim: #8b949e;', '--text-dim: #a68a64;')
css = css.replace('--border-color: rgba(255, 255, 255, 0.15);', '--border-color: rgba(255, 183, 3, 0.15);')
css = css.replace('--glass-bg: rgba(22, 27, 34, 0.65);', '--glass-bg: rgba(43, 29, 22, 0.85);')
css = css.replace('--glass-shadow: 0 16px 32px 0 rgba(0, 0, 0, 0.45);', '--glass-shadow: 0 16px 32px 0 rgba(0, 0, 0, 0.6);')
css = css.replace('--glass-border: 1px solid rgba(255, 255, 255, 0.12);', '--glass-border: 1px solid rgba(255, 183, 3, 0.12);')

new_body = """body {
    background-color: var(--bg-main) !important;
    background-image: url('../images/cyber_bogolan.png') !important;
    background-size: 500px;
    background-blend-mode: soft-light;
    margin: 0;
    color: var(--text-high) !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.6;
}"""

css = re.sub(r'body\s*\{[^}]+\}', new_body, css, count=1)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print("CSS updated.")

# 2. Update Web interface lore weapons
html_path = r'c:\Users\USER\digital-day-ctf\templates\market\view.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('La Garde Royale', 'Lance Empoisonnée')
html = html.replace("Trésorerie de l'Empire", "Vision du Marabout")
html = html.replace('Marché des Manuscrits', 'Parchemins de Djenné')
html = html.replace('Sceau de Protection', 'Bouclier Cauri')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated.")
