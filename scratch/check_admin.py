import sqlite3
conn = sqlite3.connect('files/rootthebox.db')
c = conn.cursor()

# Admin user info
c.execute("SELECT id, _handle, password, _locked, logins FROM user WHERE _handle='admin'")
row = c.fetchone()
if row:
    uid, handle, pw, locked, logins = row
    print("=== COMPTE ADMIN ===")
    print("ID      :", uid)
    print("Handle  :", handle)
    print("Hash    :", pw)
    print("Locked  :", locked)
    print("Logins  :", logins)
    print("2bad ok :", "2bad" in (pw or ""))
else:
    print("ERREUR: Utilisateur admin introuvable!")

# Permissions
c.execute("SELECT name FROM permission WHERE user_id=1")
perms = c.fetchall()
print("Perms   :", [p[0] for p in perms])

# All users
print("\n=== TOUS LES UTILISATEURS ===")
c.execute("SELECT id, _handle, _locked FROM user")
for row in c.fetchall():
    print(" -", row)

conn.close()
