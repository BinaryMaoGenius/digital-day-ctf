"""
Reset password admin - utilise exactement le meme algorithme que RootTheBox.
PBKDF2.crypt avec 0x2BAD (11181) iterations.
"""
import sqlite3
import sys
import os
sys.path.insert(0, os.getcwd())

from pbkdf2 import PBKDF2

DB_PATH = "files/rootthebox.db"
TARGET_HANDLE = "admin"
NEW_PASSWORD = "digitalday2024"
ITERATE = 0x2BAD  # Meme constante que models/User.py

def hash_password(password):
    """Hash identique a User._hash_password()"""
    return PBKDF2.crypt(password, iterations=ITERATE)

def main():
    if not os.path.exists(DB_PATH):
        print("ERREUR: Base de donnees introuvable: %s" % DB_PATH)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lire le hash actuel
    cursor.execute("SELECT id, _handle, password FROM user WHERE _handle=?", (TARGET_HANDLE,))
    row = cursor.fetchone()

    if not row:
        print("ERREUR: Utilisateur '%s' introuvable." % TARGET_HANDLE)
        cursor.execute("SELECT id, _handle FROM user")
        print("Utilisateurs: %s" % cursor.fetchall())
        conn.close()
        sys.exit(1)

    user_id, handle, old_hash = row
    print("Utilisateur: ID=%d, Handle=%s" % (user_id, handle))
    print("Ancien hash: %s" % old_hash[:40])

    # Generer le bon hash
    new_hash = hash_password(NEW_PASSWORD)
    print("Nouveau hash: %s" % new_hash[:40])
    print("Iterations: 0x%X (%d)" % (ITERATE, ITERATE))

    # Verification: simuler validate_password
    verify = (new_hash == PBKDF2.crypt(NEW_PASSWORD, new_hash))
    print("Verification hash: %s" % ("OK" if verify else "ECHEC"))

    if not verify:
        print("ERREUR: Le hash genere n'est pas valide!")
        conn.close()
        sys.exit(1)

    # Mettre a jour en base
    cursor.execute("UPDATE user SET password=? WHERE id=?", (new_hash, user_id))
    conn.commit()
    conn.close()

    print("\nSUCCES: Mot de passe 'admin' reinitialise!")
    print("URL: http://localhost:8888/login")
    print("Utilisateur: %s" % TARGET_HANDLE)
    print("Mot de passe: %s" % NEW_PASSWORD)

if __name__ == "__main__":
    main()
