import sqlite3
from pbkdf2 import PBKDF2

conn = sqlite3.connect('files/rootthebox.db')
c = conn.cursor()
c.execute("SELECT password FROM user WHERE _handle='admin'")
stored_hash = c.fetchone()[0]
conn.close()

password_to_test = "digitalday2024"

# Exactement comme validate_password() dans User.py :
# return self.password == PBKDF2.crypt(attempt, self.password)
computed = PBKDF2.crypt(password_to_test, stored_hash)
result = stored_hash == computed

print("Hash en base  :", stored_hash)
print("Hash calcule  :", computed)
print("Correspond    :", result)

if result:
    print("\nSUCCES: Le mot de passe 'digitalday2024' est CORRECT pour admin")
else:
    print("\nECHEC: Le mot de passe ne correspond pas!")
