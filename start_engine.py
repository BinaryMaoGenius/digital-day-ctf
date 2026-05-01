import subprocess
import time
import sys
import os

# Liste des services à lancer
services = [
    {"name": "RootTheBox", "path": "rootthebox.py", "args": ["--start"], "cwd": "."},
    {"name": "Target-Segou", "path": "targets/segou/app.py", "args": [], "cwd": "."},
    {"name": "Target-Bougouni", "path": "targets/bougouni/app.py", "args": [], "cwd": "."},
    {"name": "Target-Taoudeni", "path": "targets/taoudeni/app.py", "args": [], "cwd": "."},
    {"name": "Target-Tessalit", "path": "targets/tessalit/app.py", "args": [], "cwd": "."},
    {"name": "Target-San", "path": "targets/san/app.py", "args": [], "cwd": "."},
    {"name": "Target-Gao", "path": "targets/gao/app.py", "args": [], "cwd": "."},
]

processes = []

print("--- DÉMARRAGE DU MOTEUR DE L'ÉQUATION DU MANDÉ ---")

for service in services:
    print(f"[*] Lancement de {service['name']}...")
    try:
        # On lance chaque service dans un processus séparé
        p = subprocess.Popen(
            [sys.executable, service['path']] + service['args'],
            cwd=service['cwd'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        processes.append((service['name'], p))
        time.sleep(1) # Un court délai pour éviter les collisions au démarrage
    except Exception as e:
        print(f"[!] Erreur lors du lancement de {service['name']}: {e}")

print("\n--- TOUS LES SERVICES SONT EN COURS D'EXÉCUTION ---")
print("Plateforme : http://localhost:8888")
print("Moteurs techniques : Ports 8001 à 8006")
print("\nAppuyez sur Ctrl+C pour tout arrêter (ou fermez ce terminal).")

try:
    while True:
        # On garde le script en vie et on check si un process meurt
        for name, p in processes:
            if p.poll() is not None:
                print(f"[!] ALERTE : {name} s'est arrêté de manière inattendue.")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n[!] Arrêt chirurgical de tous les services...")
    for name, p in processes:
        p.terminate()
    print("[+] Système arrêté.")
