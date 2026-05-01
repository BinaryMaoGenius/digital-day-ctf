# -*- coding: utf-8 -*-
"""
Le Grimoire de Sankoré
----------------------
Ce script protège l'accès aux manuscrits sacrés.
Seul l'Érudit qui saura inverser le flux de la pensée pourra entrer.
"""

import sys

def transformer(message):
    # L'algorithme des Anciens
    cle = "MANDE"
    resultat = []
    for i, char in enumerate(message):
        # Une transformation mystique basée sur la clé et la position
        v = (ord(char) ^ ord(cle[i % len(cle)])) + (i * 2)
        resultat.append(v)
    return resultat

def verifier():
    print("--- BIENVENUE À LA BIBLIOTHÈQUE DE SANKORÉ ---")
    entree = input("Entrez la parole sacrée pour débloquer le grimoire : ")
    
    # Résultat attendu (Flag encodé)
    # flag{SANKORE_REVERSE_MASTER_2024}
    attendu = [37, 33, 49, 36, 17, 107, 73, 94, 91, 107, 105, 110, 93, 131, 114, 113, 130, 115, 131, 134, 134, 155, 130, 143, 161, 153, 161, 159, 131, 126, 128, 128, 191]
    
    if transformer(entree) == attendu:
        print("\n[SUCCÈS] La sagesse vous appartient. La porte s'ouvre...")
        print("Votre flag est : " + entree)
    else:
        print("\n[ÉCHEC] Les ombres rejettent votre parole. Essayez encore.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--encode":
        # Utilitaire pour le créateur (moi)
        msg = input("Message à encoder : ")
        print(transformer(msg))
    else:
        verifier()
