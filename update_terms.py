import os

for root, _, files in os.walk(r"c:\Users\USER\digital-day-ctf\templates"):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            new_content = content.replace('_("$")', '"C "').replace("_('$')", "'C '").replace('{{_("$")}}', '{{ "C " }}')
            new_content = new_content.replace('{{ _("Money") }}', '{{ _("Cauris") }}').replace("{{ _('Money') }}", "{{ _('Cauris') }}")
            new_content = new_content.replace('{{ _("Black Market") }}', '{{ _("Marché Clandestin") }}')
            new_content = new_content.replace('{{ _("Botnet") }}', '{{ _("Armée de Génies") }}')
            new_content = new_content.replace('{{ _("Bots") }}', '{{ _("Génies") }}')
            new_content = new_content.replace('{{ _("Federal Reserve") }}', '{{ _("Trésorerie de l\'Empire") }}')
            new_content = new_content.replace('{{ _("S.W.A.T.") }}', '{{ _("Garde Royale") }}')
            new_content = new_content.replace('{{ _("Source Code Market") }}', '{{ _("Marché des Manuscrits") }}')
            new_content = new_content.replace('{{ _("Password Security") }}', '{{ _("Sceau de Protection") }}')
            
            if new_content != content:
                print(f"Updated {path}")
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
