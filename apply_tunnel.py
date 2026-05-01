import paramiko

HOSTNAME = '192.168.101.30'
USERNAME = 'digitalday'
PASSWORD = 'digitalday2026'
TOKEN = 'eyJhIjoiYmRhNGUzNWQ3YTE2MjE2MDljNGE5MmYzNDgxYjk4NGIiLCJ0IjoiZTczNTE1NjQtMDA3Ny00MTdlLTlkOTMtMWM5Y2ExYzdmZmI2IiwicyI6Ik4yWXpZVE00TURndFpqa3pNaTAwWldOakxXRXpNVEF0WWpJNE9USTRPREpsWVRaayJ9'

def apply():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        
        # Update .env
        cmd_env = f'cd digital-day-ctf && echo "CLOUDFLARE_TOKEN={TOKEN}" > .env'
        ssh.exec_command(cmd_env)
        
        # Restart tunnel
        cmd_restart = 'cd digital-day-ctf && echo "digitalday2026" | sudo -S docker-compose up -d tunnel'
        stdin, stdout, stderr = ssh.exec_command(cmd_restart)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("[+] Tunnel token applied and service restarted!")
        ssh.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    apply()
