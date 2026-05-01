# --- SAN UPGRADE ---
import time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

PREMIUM_CSS = open('static/css/targets_premium.css', 'r').read()

inventory = {"fish": 1, "cauris": 0}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SAN | Pêche Sacrée</title>
    <style>
        {{ css | safe }}
        .cauri-stats { display: flex; justify-content: space-around; margin: 30px 0; }
        .stat-item { text-align: center; border: 1px solid var(--border-color); padding: 15px; border-radius: 8px; width: 40%; }
        .stat-val { font-size: 2rem; color: var(--accent-color); font-weight: bold; }
    </style>
</head>
<body>
    <div class="cockpit-frame">
        <div class="terminal-header">
            <div><span class="status-dot"></span> BOURSE DU SANKÉ MON</div>
            <div style="font-size: 0.8rem; color: var(--text-dim);">LATENCE: 100ms</div>
        </div>
        
        <h1>La Pêche Sacrée</h1>
        <div class="bogolan-divider"></div>
        
        <p class="lore-text">
            Le marché des cauris est instable. Les transactions se croisent dans le temps. 
            Celui qui peut être à deux endroits en même temps possédera l'étang.
        </p>

        <div class="cauri-stats">
            <div class="stat-item">
                <div style="font-size: 0.7rem; color: var(--text-dim);">POISSONS</div>
                <div class="stat-val" id="fish-val">1</div>
            </div>
            <div class="stat-item">
                <div style="font-size: 0.7rem; color: var(--text-dim);">CAURIS</div>
                <div class="stat-val" id="cauri-val">0</div>
            </div>
        </div>

        <div id="msg" style="text-align: center; min-height: 20px; font-family: monospace; color: var(--success); margin-bottom: 20px;"></div>

        <button class="action-btn" style="width: 100%;" onclick="exchange()">DÉCLENCHER L'ÉCHANGE RAPIDE</button>
        
        <div style="margin-top: 20px; font-size: 0.7rem; color: var(--text-dim);">OBJECTIF : 10 CAURIS</div>
    </div>

    <script>
        function exchange() {
            fetch('/api/exchange', {method: 'POST'})
            .then(r => r.json())
            .then(d => {
                document.getElementById('msg').innerText = d.message;
                document.getElementById('fish-val').innerText = d.fish;
                document.getElementById('cauri-val').innerText = d.cauris;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, css=PREMIUM_CSS)

@app.route('/api/exchange', methods=['POST'])
def exchange():
    if inventory['fish'] > 0:
        time.sleep(0.1)
        inventory['fish'] -= 1
        inventory['cauris'] += 1
        msg = "Transaction validée."
        if inventory['cauris'] >= 10: msg = "FLAWLESS : flag{race_condition_sanke_mon_2024}"
        return jsonify({"message": msg, "fish": inventory['fish'], "cauris": inventory['cauris']})
    return jsonify({"message": "Fonds insuffisants", "fish": inventory['fish'], "cauris": inventory['cauris']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005, threaded=True)
