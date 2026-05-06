import paramiko
import sys

HOSTNAME = '192.168.101.30'
USERNAME = 'digitalday'
PASSWORD = 'digitalday2026'

def run_cmd(cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        
        full_cmd = f'echo "digitalday2026" | sudo -S bash -c "{cmd}"'
        print(f"[*] Executing: {full_cmd}")
        stdin, stdout, stderr = ssh.exec_command(full_cmd)
        
        print("--- STDOUT ---")
        print(stdout.read().decode())
        print("--- STDERR ---")
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_cmd(" ".join(sys.argv[1:]))
    else:
        # Default: check all logs
        run_cmd("cd digital-day-ctf && docker-compose logs --tail=50")
