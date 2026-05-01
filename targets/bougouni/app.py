from flask import Flask, request, jsonify, make_response, render_template_string
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mande_secret_key_2024'

PREMIUM_CSS = open('static/css/targets_premium.css', 'r').read()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BOUGOUNI | Marché des Ombres</title>
    <style>
        {{ css | safe }}
        .token-display { background: #000; padding: 15px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; word-break: break-all; border: 1px dashed var(--accent-color); margin: 20px 0; }
    </style>
</head>
<body>
    <div class="cockpit-frame">
        <div class="terminal-header">
            <div><span class="status-dot"></span> SYSTÈME DE GESTION DU MARCHÉ</div>
            <div style="font-size: 0.8rem; color: var(--text-dim);">SECTEUR: SUD-BOUGOUNI</div>
        </div>
        
        <h1>L'Identité Numérique</h1>
        <div class="bogolan-divider"></div>
        
        <p class="lore-text">
            Au marché de Bougouni, tout se négocie, même l'identité. Les jetons de passage sont la monnaie courante. 
            Modifiez votre essence pour accéder aux archives interdites.
        </p>

        <div id="status-box" class="lore-text" style="color: var(--accent-color);">
            [!] STATUT : Visiteur (Accès Limité)
        </div>

        <button class="action-btn" onclick="login()">GÉNÉRER UN JETON VISITEUR</button>
        <button class="action-btn" style="background: transparent; border: 1px solid var(--accent-color); color: var(--accent-color);" onclick="checkSecret()">ACCÉDER AUX ARCHIVES</button>
        
        <div id="token-box" class="token-display" style="display:none;"></div>
        
        <div id="secret-data" class="lore-text" style="margin-top: 20px; display:none;"></div>
    </div>

    <script>
        function login() {
            fetch('/login')
            .then(r => r.json())
            .then(d => {
                const box = document.getElementById('token-box');
                box.style.display = 'block';
                box.innerHTML = "TOKEN REÇU : " + document.cookie;
                alert("Jeton visiteur enregistré dans vos cookies.");
            });
        }

        function checkSecret() {
            fetch('/api/secret')
            .then(r => r.json())
            .then(d => {
                const res = document.getElementById('secret-data');
                res.style.display = 'block';
                if(d.status === 'success') {
                    res.innerHTML = "<span style='color:var(--success)'>[ACCÈS AUTORISÉ]</span><br>FLAG : " + d.flag;
                } else {
                    res.innerHTML = "<span style='color:red'>[ACCÈS REFUSÉ]</span><br>" + d.message;
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

@app.route('/login')
def login():
    token = jwt.encode({
        'user': 'guest_hunter',
        'role': 'guest',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    resp = make_response(jsonify({"status": "success", "message": "Connecté"}))
    resp.set_cookie('access_token', token)
    return resp

@app.route('/api/secret')
def secret():
    token = request.cookies.get('access_token')
    if not token:
        return jsonify({"status": "error", "message": "Non authentifié."}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if data.get('role') == 'admin':
            return jsonify({"status": "success", "flag": "flag{jwt_identity_theft_market_real}"})
        else:
            return jsonify({"status": "error", "message": "Droits insuffisants (Role: guest)."}), 403
    except Exception:
        return jsonify({"status": "error", "message": "Jeton corrompu."}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
