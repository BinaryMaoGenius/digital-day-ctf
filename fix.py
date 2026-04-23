import re

with open("templates/menu/user.html", "r", encoding="utf-8") as f:
    c = f.read()

replacement = """<a href="/user/settings" style="color: var(--text-primary); text-decoration: none;" title="Paramètres">
            <i class="fa fa-gears" style="font-size: 1.2rem;"></i>
        </a>
        <a href="/logout" style="color: var(--danger); text-decoration: none; margin-left: 15px;" title="Déconnexion">
            <i class="fa fa-sign-out" style="font-size: 1.2rem;"></i>
        </a>"""

c = re.sub(r'<div class="dropdown">.*?</div>', replacement, c, flags=re.DOTALL | re.IGNORECASE)

with open("templates/menu/user.html", "w", encoding="utf-8") as f:
    f.write(c)
