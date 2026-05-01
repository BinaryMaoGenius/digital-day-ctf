import paramiko
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.101.30', username='digitalday', password='digitalday2026', timeout=10)
    print("SUCCESS")
    ssh.close()
except Exception as e:
    print(f"FAILED: {e}")
