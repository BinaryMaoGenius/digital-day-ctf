import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

PREMIUM_CSS = open('static/css/targets_premium.css', 'r').read()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>TAOUDÉNI | Surveillance Tactique</title>
    <style>
        {{ css | safe }}
        .radar-box { height: 200px; background: radial-gradient(circle, #1a1a1a 0%, #000 100%); border: 1px solid var(--border-color); border-radius: 50%; position: relative; overflow: hidden; margin: 20px auto; width: 200px; }
        .radar-line { position: absolute; width: 100%; height: 2px; background: var(--accent-color); top: 50%; animation: rotate 4s linear infinite; }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="cockpit-frame">
        <div class="terminal-header">
            <div><span class="status-dot" style="background: #ff0000; box-shadow: 0 0 10px #ff0000;"></span> UNITÉ DE FORAGE - TAOUDÉNI</div>
            <div style="font-size: 0.8rem; color: var(--text-dim);">PROFOND: -400M</div>
        </div>
        
        <div class="radar-box"><div class="radar-line"></div></div>

        <h1>Le Paradoxe de l'Or Blanc</h1>
        <div class="bogolan-divider"></div>
        
        <p class="lore-text">
            Le réseau des mines est un labyrinthe de sondes isolées. L'outil de diagnostic peut atteindre n'importe quel point... à condition de savoir où pointer.
        </p>

        <div id="diag-res" style="background: rgba(0,0,0,0.5); padding: 15px; font-family: monospace; font-size: 0.8rem; min-height: 50px; border: 1px solid var(--border-color);">
            [ SYSTÈME PRÊT ] : En attente d'URL de diagnostic...
        </div>

        <input type="text" id="probe_url" class="input-field" placeholder="http://sonde-externe.mande/status">
        <button class="action-btn" onclick="scan()">LANCER LE DIAGNOSTIC</button>
    </div>

    <script>
        function scan() {
            const url = document.getElementById('probe_url').value;
            const res = document.getElementById('diag-res');
            res.innerHTML = "> Établissement de la connexion proxy...";
            
            fetch('/proxy?url=' + encodeURIComponent(url))
            .then(r => r.text())
            .then(d => {
                res.innerText = d;
            })
            .catch(e => {
                res.innerHTML = "> ÉCHEC : La sonde est injoignable.";
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, css=PREMIUM_CSS)

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url', '')
    if not target_url: return "Erreur : URL manquante"
    try:
        if "localhost" in target_url: return "ACCÈS INTERDIT : Protocole de l'Empire en vigueur."
        response = requests.get(target_url, timeout=3)
        return response.text
    except Exception as e:
        return f"Erreur de communication : {str(e)}"

@app.route('/internal/metadata')
def internal():
    if request.remote_addr != '127.0.0.1': return "Accès réservé au réseau interne.", 403
    return jsonify({"flag": "flag{ssrf_master_taoudeni_final_access_2024}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)
