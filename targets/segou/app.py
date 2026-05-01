from flask import Flask, request, jsonify, render_template_string
import sqlite3
import time

app = Flask(__name__)

# Design System Intégré (Zugenberg Style)
from premium_css import PREMIUM_CSS

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SÉGOU | Registre Royal</title>
    <style>
        {{ css | safe }}
        .archive-data { background: rgba(0,0,0,0.4); padding: 20px; border-radius: 8px; border-left: 4px solid var(--accent-color); margin-top: 20px; }
        .glitch-text { animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; text-shadow: 0 0 10px var(--accent-color); } 100% { opacity: 0.8; } }
    </style>
</head>
<body>
    <div class="cockpit-frame">
        <div class="terminal-header">
            <div><span class="status-dot"></span> <span style="letter-spacing: 2px;">SYSTÈME D'ARCHIVE ROYAL - SÉGOU</span></div>
            <div style="font-size: 0.8rem; color: var(--text-dim);">COORD: 13.43 / -6.27</div>
        </div>
        
        <h1>L'Héritage des Balanzans</h1>
        <div class="bogolan-divider"></div>
        
        <p class="lore-text">
            Le registre des citoyens de Ségou est scellé par un protocole binaire ancien. 
            Le gardien ne répond qu'à des requêtes numériques précises. Si le temps se fige, la vérité émerge.
        </p>

        <div class="archive-data">
            <p style="color: var(--accent-color); margin: 0;">[ ANALYSE DES FLUX ]</p>
            <p id="result" style="font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;">
                En attente d'identification du citoyen...
            </p>
        </div>

        <input type="text" id="citizen_id" class="input-field" placeholder="ID CITOYEN (ex: 42)" onkeypress="if(event.key === 'Enter') query()">
        <button class="action-btn" onclick="query()">INTERROGER LE GARDIEN</button>
        
        <div style="margin-top: 30px; font-size: 0.7rem; color: var(--text-dim);">
            SIGNAL DE CONFLUENCE : <span class="glitch-text">TAD-3-INTERNAL</span>
        </div>
    </div>

    <script>
        function query() {
            const id = document.getElementById('citizen_id').value;
            const resDiv = document.getElementById('result');
            resDiv.innerHTML = "> Transmission en cours...";
            
            fetch('/api/citizen?id=' + id)
            .then(r => r.json())
            .then(d => {
                if(d.status === 'success') {
                    resDiv.innerHTML = "> RÉSULTAT : Citoyen " + d.data.name + " (" + d.data.role + ") identifié.";
                } else {
                    resDiv.innerHTML = "> ERREUR : " + d.message;
                }
            })
            .catch(e => {
                resDiv.innerHTML = "> ÉCHEC : Le gardien est resté silencieux.";
            });
        }
    </script>
</body>
</html>
"""

def init_db():
    conn = sqlite3.connect('segou_registry.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('CREATE TABLE users (id INTEGER, username TEXT, description TEXT, password TEXT)')
    c.execute("INSERT INTO users VALUES (1, 'admin', 'Gardien du Registre', 'flag{blind_sqli_segou_king_secret}')")
    c.execute("INSERT INTO users VALUES (42, 'biton', 'Roi Biton Coulibaly', 'segou_city_1712')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, css=PREMIUM_CSS)

@app.route('/api/citizen')
def get_citizen():
    citizen_id = request.args.get('id', '')
    query = f"SELECT username, description FROM users WHERE id = {citizen_id}"
    conn = sqlite3.connect('segou_registry.db')
    c = conn.cursor()
    try:
        c.execute(query)
        res = c.fetchone()
        conn.close()
        if res:
            return jsonify({"status": "success", "data": {"name": res[0], "role": res[1]}})
        else:
            return jsonify({"status": "error", "message": "Citoyen introuvable"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": "Erreur interne du gardien"}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8001)
