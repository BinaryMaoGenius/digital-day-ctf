import paramiko

HOSTNAME = '192.168.101.30'
USERNAME = 'digitalday'
PASSWORD = 'digitalday2026'

def check():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        
        cmd = 'echo "digitalday2026" | sudo -S docker ps -a --format "{{.Names}}\t{{.Status}}"'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        ssh.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    check()
