# -*- coding: utf-8 -*-
import sys

def mande_logic(data):
    # Un algorithme de transformation asymétrique
    key = "MANSA_MUSA_1324"
    result = []
    for i in range(len(data)):
        char_code = ord(data[i])
        key_code = ord(key[i % len(key)])
        # Chirurgie binaire : XOR + décalage circulaire
        transformed = (char_code ^ key_code) + (i % 5)
        result.append(hex(transformed)[2:])
    return "-".join(result)

def check_secret(attempt):
    # Le secret attendu (encodé)
    # flag{SANKORE_REVERSE_MASTER_2024}
    vault = "23-25-2f-2c-3e-1b-0-1d-15-2a-1e-2-12-0-1c-16-10-1c-16-10-2b-10-0-1a-1d-1-2b-4d-45-42-42"
    return mande_logic(attempt) == vault

def main():
    print("--- UNIVERSITÉ DE SANKORÉ : ACCÈS AU GRIMOIRE ---")
    print("Le savoir est une clé qui ne tourne que dans un sens.")
    secret = input("Entrez le mot de passe du Doyen : ")
    
    if check_secret(secret):
        print("[SUCCÈS] Les portes de la connaissance s'ouvrent à vous.")
        print("FLAG : " + secret)
    else:
        print("[ÉCHEC] Votre esprit n'est pas encore prêt pour cette vérité.")

if __name__ == "__main__":
    main()
