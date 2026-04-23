"""
Script autonome pour réinitialiser le mot de passe admin
directement via sqlite3 (sans dépendances Tornado/SQLAlchemy).
Utilise le même algorithme de hachage (pbkdf2) que RootTheBox.
"""
import sqlite3
import os
import sys
from pbkdf2 import PBKDF2

DB_PATH = "files/rootthebox.db"
TARGET_HANDLE = "admin"
NEW_PASSWORD = "digitalday2024"

def hash_password(password):
    """Recrée le hash PBKDF2 utilisé par RootTheBox (models/User.py)"""
    # RootTheBox utilise PBKDF2.crypt() par défaut
    return PBKDF2.crypt(password)

def main():
    if not os.path.exists(DB_PATH):
        print(f"ERREUR: Base de données introuvable: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Trouver les colonnes de la table user
    cursor.execute("PRAGMA table_info(user)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Colonnes disponibles: {columns}")

    # Chercher l'utilisateur admin
    handle_col = None
    for col in ["handle", "_handle", "username", "name"]:
        if col in columns:
            handle_col = col
            break

    if not handle_col:
        print("ERREUR: Impossible de trouver la colonne du nom d'utilisateur")
        conn.close()
        sys.exit(1)

    # Trouver le champ password
    pass_col = None
    for col in ["_password", "password", "passwd"]:
        if col in columns:
            pass_col = col
            break

    if not pass_col:
        print("ERREUR: Impossible de trouver la colonne du mot de passe")
        conn.close()
        sys.exit(1)

    print(f"Colonne handle: {handle_col}, Colonne password: {pass_col}")

    # Chercher l'utilisateur admin
    cursor.execute(f"SELECT id, {handle_col}, {pass_col} FROM user WHERE {handle_col}=?", (TARGET_HANDLE,))
    row = cursor.fetchone()

    if not row:
        print(f"ERREUR: Utilisateur '{TARGET_HANDLE}' introuvable.")
        # Lister tous les utilisateurs
        cursor.execute(f"SELECT id, {handle_col} FROM user")
        users = cursor.fetchall()
        print(f"Utilisateurs disponibles: {users}")
        conn.close()
        sys.exit(1)

    user_id, handle, old_password = row
    print(f"Utilisateur trouvé: ID={user_id}, Handle={handle}")
    print(f"Ancien hash: {old_password[:30]}...")

    # Générer le nouveau hash
    new_hash = hash_password(NEW_PASSWORD)
    print(f"Nouveau hash: {new_hash[:30]}...")

    # Mettre à jour le mot de passe
    cursor.execute(f"UPDATE user SET {pass_col}=? WHERE id=?", (new_hash, user_id))
    conn.commit()
    conn.close()

    print(f"\n✅ SUCCÈS: Mot de passe de '{TARGET_HANDLE}' réinitialisé à '{NEW_PASSWORD}'")
    print(f"URL: http://localhost:8888/login")
    print(f"Utilisateur: {TARGET_HANDLE}")
    print(f"Mot de passe: {NEW_PASSWORD}")

if __name__ == "__main__":
    main()
