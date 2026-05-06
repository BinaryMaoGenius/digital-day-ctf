import paramiko
import os

HOSTNAME = '192.168.101.30'
USERNAME = 'digitalday'
PASSWORD = 'digitalday2026'
REMOTE_PATH = 'digital-day-ctf'

FILES_TO_SYNC = [
    ('models/GameLevel.py', 'models/GameLevel.py'),
    ('models/Box.py', 'models/Box.py'),
    ('models/IpAddress.py', 'models/IpAddress.py'),
    ('models/Corporation.py', 'models/Corporation.py'),
    ('deploy/nginx/nginx.conf', 'deploy/nginx/nginx.conf'),
    ('static/css/digital-day.css', 'static/css/digital-day.css'),
    ('templates/missions/box.html', 'templates/missions/box.html'),
    ('docker-compose.yml', 'docker-compose.yml'),
    ('setup/digital_day_missions_fr.xml', 'setup/digital_day_missions_fr.xml'),
    ('targets/', 'targets/'),
    ('static/targets/', 'static/targets/'),
]

def sync():
    try:
        print(f"[*] Connecting to {HOSTNAME}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        
        sftp = ssh.open_sftp()
        
        def put_dir(local_dir, remote_dir):
            ssh.exec_command(f"mkdir -p {remote_dir}")
            for item in os.listdir(local_dir):
                l_path = os.path.join(local_dir, item)
                r_path = remote_dir + '/' + item
                if os.path.isdir(l_path):
                    put_dir(l_path, r_path)
                else:
                    sftp.put(l_path, r_path)

        for local_file, remote_file in FILES_TO_SYNC:
            local_full_path = os.path.join(os.getcwd(), local_file)
            remote_full_path = REMOTE_PATH + '/' + remote_file
            
            if os.path.isdir(local_full_path):
                print(f"[*] Uploading directory {local_file} -> {remote_full_path}...")
                put_dir(local_full_path, remote_full_path)
            else:
                print(f"[*] Uploading file {local_file} -> {remote_full_path}...")
                sftp.put(local_full_path, remote_full_path)
        
        sftp.close()
        
        print("[*] Importing mission XML...")
        import_cmd = f'cd {REMOTE_PATH} && python3 rootthebox.py --xml=setup/digital_day_missions_fr.xml'
        ssh.exec_command(import_cmd)

        print("[*] Rebuilding and restarting containers...")
        # Rebuild and restart using the most compatible syntax
        cmd = f'cd {REMOTE_PATH} && echo "digitalday2026" | sudo -S docker-compose up -d --build'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("[+] Sync, XML Import and Restart completed successfully!")
        ssh.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == '__main__':
    sync()
