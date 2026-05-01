import paramiko
import time
import sys

# Server Details
HOSTNAME = '192.168.101.30'
USERNAME = 'digitalday'
PASSWORD = 'digitalday2026'

def execute_command(ssh, command):
    print(f"\n[+] Executing: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    
    if command.startswith('sudo'):
        stdin.write(PASSWORD + '\n')
        stdin.flush()

    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            data = stdout.channel.recv(1024).decode('utf-8', errors='ignore')
            try:
                sys.stdout.write(data)
                sys.stdout.flush()
            except UnicodeEncodeError:
                sys.stdout.write(data.encode('ascii', 'ignore').decode('ascii'))
                sys.stdout.flush()
        if stdout.channel.recv_stderr_ready():
            data = stdout.channel.recv_stderr(1024).decode('utf-8', errors='ignore')
            try:
                sys.stderr.write(data)
                sys.stderr.flush()
            except UnicodeEncodeError:
                sys.stderr.write(data.encode('ascii', 'ignore').decode('ascii'))
                sys.stderr.flush()
        time.sleep(0.1)

    print(f"\n[!] Command finished with exit status: {stdout.channel.recv_exit_status()}")

def deploy():
    try:
        print(f"[*] Connecting to {USERNAME}@{HOSTNAME}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD, timeout=10)
        print("[+] Connected successfully!")
        
        # 1. Update and install dependencies
        execute_command(ssh, 'echo "digitalday2026" | sudo -S apt-get update')
        execute_command(ssh, 'echo "digitalday2026" | sudo -S apt-get install -y git docker.io docker-compose')
        
        # 2. Network Persistence (Netplan)
        print("[*] Configuring network persistence...")
        # Get primary interface name (excluding lo)
        stdin, stdout, stderr = ssh.exec_command("ip -br link show | grep -v lo | awk '{print $1}' | head -n 1")
        interface = stdout.read().decode().strip()
        print(f"[+] Detected interface: {interface}")
        
        if interface:
            netplan_config = f"""network:
  version: 2
  renderer: networkd
  ethernets:
    {interface}:
      addresses:
        - 192.168.101.30/24
      routes:
        - to: default
          via: 192.168.101.2
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]"""
            
            # Write netplan file
            cmd = f'echo "digitalday2026" | sudo -S bash -c "cat <<EOF > /etc/netplan/00-installer-config.yaml\n{netplan_config}\nEOF"'
            execute_command(ssh, cmd)
            execute_command(ssh, 'echo "digitalday2026" | sudo -S netplan apply')
            print("[+] Network persistence applied!")

        # 3. Clone or update repository
        # If directory exists, git pull, else git clone
        setup_repo_cmd = """
        if [ -d "digital-day-ctf" ]; then
            cd digital-day-ctf && git pull origin master
        else
            git clone https://github.com/BinaryMaoGenius/digital-day-ctf.git
        fi
        """
        execute_command(ssh, setup_repo_cmd)
        
        # 3. Create .env file for environment variables (like Cloudflare token)
        execute_command(ssh, 'echo "CLOUDFLARE_TOKEN=" > digital-day-ctf/.env')
        
        # 4. Stop existing containers (if any), build and start new ones
        execute_command(ssh, 'cd digital-day-ctf && echo "digitalday2026" | sudo -S docker-compose down')
        execute_command(ssh, 'cd digital-day-ctf && echo "digitalday2026" | sudo -S docker-compose build')
        execute_command(ssh, 'cd digital-day-ctf && echo "digitalday2026" | sudo -S docker-compose up -d')
        
        print("[*] Deployment completed!")
        ssh.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    deploy()
