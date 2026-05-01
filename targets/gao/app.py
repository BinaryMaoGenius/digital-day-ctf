from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

from premium_css import PREMIUM_CSS

# État simulé du système de fichiers
FILESYSTEM = {
    "/home/askia_guest/note.txt": "Bienvenue soldat. Le binaire 'tax_collector' est en test. Signalez tout bug au doyen.",
    "/root/flag.txt": "flag{suid_path_hijack_gao_root_2024}"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GAO | Console Askia</title>
    <style>
        {{ css | safe }}
        #terminal-output { height: 300px; overflow-y: auto; background: #000; padding: 15px; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: var(--success); border: 1px solid var(--border-color); margin-bottom: 10px; }
        .prompt { color: var(--accent-color); }
    </style>
</head>
<body>
    <div class="cockpit-frame" style="max-width: 800px;">
        <div class="terminal-header">
            <div><span class="status-dot"></span> SSH: askia_guest@gao-central</div>
            <div style="font-size: 0.8rem; color: var(--text-dim);">IP: 10.0.0.14</div>
        </div>
        
        <h1>L'Ascension des Askia</h1>
        <div class="bogolan-divider"></div>
        
        <div id="terminal-output">
            Bienvenue sur le système central de Gao (Askia-OS v4.2)<br>
            Tapez 'help' pour la liste des commandes.<br><br>
        </div>

        <div style="display: flex; align-items: center;">
            <span class="prompt">askia_guest@gao:~$ &nbsp;</span>
            <input type="text" id="cmd-input" class="input-field" style="border:none; background:transparent; padding:0;" autofocus onkeypress="if(event.key === 'Enter') execute()">
        </div>
    </div>

    <script>
        function execute() {
            const input = document.getElementById('cmd-input');
            const output = document.getElementById('terminal-output');
            const cmd = input.value;
            
            output.innerHTML += "<span class='prompt'>askia_guest@gao:~$</span> " + cmd + "<br>";
            
            fetch('/api/exec?cmd=' + encodeURIComponent(cmd))
            .then(r => r.json())
            .then(d => {
                output.innerHTML += d.output + "<br>";
                output.scrollTop = output.scrollHeight;
            });
            
            input.value = "";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, css=PREMIUM_CSS)

@app.route('/api/exec')
def exec_cmd():
    cmd = request.args.get('cmd', '').split()
    if not cmd: return jsonify({"output": ""})
    
    base = cmd[0].lower()
    
    if base == "help":
        return jsonify({"output": "Commandes disponibles: ls, cat, whoami, tax_collector, clear"})
    elif base == "ls":
        return jsonify({"output": "note.txt &nbsp;&nbsp; tax_collector"})
    elif base == "whoami":
        return jsonify({"output": "askia_guest"})
    elif base == "cat":
        if len(cmd) < 2: return jsonify({"output": "Usage: cat [fichier]"})
        filename = cmd[1]
        if "flag.txt" in filename: return jsonify({"output": "cat: /root/flag.txt: Permission non accordée"})
        return jsonify({"output": FILESYSTEM.get("/home/askia_guest/note.txt", "Fichier introuvable")})
    elif base == "tax_collector":
        # Simule un binaire SUID qui permet de lire n'importe quoi si on sait l'utiliser
        if "--read-root" in cmd:
            return jsonify({"output": f"Lecture sécurisée de /root/flag.txt...<br>CONTENU: {FILESYSTEM['/root/flag.txt']}"})
        return jsonify({"output": "Usage: tax_collector --calculate [amount] | --read-root (en test)"})
    elif base == "clear":
        return jsonify({"output": "<script>document.getElementById('terminal-output').innerHTML = '';</script>"})
    
    return jsonify({"output": f"Command: {base}: non trouvée"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
