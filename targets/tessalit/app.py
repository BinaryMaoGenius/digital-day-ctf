# --- TESSALIT UPGRADE ---
from flask import Flask, request, jsonify, render_template_string
import json

app = Flask(__name__)

PREMIUM_CSS = open('static/css/targets_premium.css', 'r').read()

SENTINELS = [
    {"username": "admin_sentinel", "access_code": "flag{nosql_injection_tessalit_sentinel_2024}"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>TESSALIT | Base Sentinelle</title>
    <style>{{ css | safe }}</style>
</head>
<body>
    <div class="cockpit-frame">
        <div class="terminal-header">
            <div><span class="status-dot"></span> UNITÉ NOMADE - TESSALIT</div>
            <div style="font-size: 0.8rem; color: var(--text-dim);">FREQ: 142.0 MHz</div>
        </div>
        
        <h1>La Sentinelle Nomade</h1>
        <div class="bogolan-divider"></div>
        
        <p class="lore-text">
            L'accès à la base de données nomade nécessite une clé de structure JSON. 
            Les sentinelles ne tolèrent aucune erreur... sauf celles de leur propre logique d'objet.
        </p>

        <div id="json-res" style="background: rgba(0,0,0,0.5); padding: 15px; font-family: monospace; font-size: 0.8rem; margin-bottom: 20px;">
            [ EN ATTENTE D'INJECTION ]
        </div>

        <textarea id="json_input" class="input-field" style="height: 100px;" placeholder='{"username": "admin_sentinel", "code": {"$ne": "???"}}'></textarea>
        <button class="action-btn" onclick="inject()">AUTHENTIFICATION CHIRURGICALE</button>
    </div>

    <script>
        function inject() {
            const val = document.getElementById('json_input').value;
            fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: val
            })
            .then(r => r.json())
            .then(d => {
                const res = document.getElementById('json_res');
                if(d.status === 'success') {
                    res.innerHTML = "<span style='color:var(--success)'>[SUCCÈS]</span> " + d.message + "<br>FLAG: " + d.flag;
                } else {
                    res.innerHTML = "<span style='color:red'>[ERREUR]</span> " + d.message;
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, css=PREMIUM_CSS)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        code = data.get('code')
        for s in SENTINELS:
            user_match = (s['username'] == username)
            code_match = False
            if isinstance(code, dict) and "$ne" in code:
                code_match = (s['access_code'] != code['$ne'])
            elif s['access_code'] == code:
                code_match = True
            
            if user_match and code_match:
                return jsonify({"status": "success", "message": "Accès accordé", "flag": s['access_code']})
        return jsonify({"status": "error", "message": "Négation refusée"}), 401
    except: return jsonify({"status": "error", "message": "Structure invalide"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)
