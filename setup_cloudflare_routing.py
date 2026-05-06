import os
import requests
import json

API_TOKEN = os.environ.get("CLOUDFLARE_TOKEN", "")
DOMAIN = "digitalday2026.com"
SUBDOMAIN = "ctf"
TARGET_SERVICE = "http://nginx:80"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def setup_cloudflare():
    # 1. Get Account ID
    print("[*] Retrieving Account ID...")
    resp = requests.get("https://api.cloudflare.com/client/v4/accounts", headers=headers)
    if resp.status_code != 200:
        print(f"[-] Failed to get accounts: {resp.text}")
        return
    
    accounts = resp.json().get("result", [])
    if not accounts:
        print("[-] No accounts found.")
        return
    
    account_id = accounts[0]["id"]
    print(f"[+] Account ID: {account_id}")

    # 2. Get Tunnel ID
    print("[*] Retrieving Tunnels...")
    resp = requests.get(f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel", headers=headers)
    if resp.status_code != 200:
        print(f"[-] Failed to get tunnels: {resp.text}")
        return
    
    tunnels = resp.json().get("result", [])
    if not tunnels:
        print("[-] No tunnels found.")
        return
    
    # We take the first active/recent tunnel
    tunnel = tunnels[0]
    tunnel_id = tunnel["id"]
    print(f"[+] Tunnel ID: {tunnel_id} ({tunnel['name']})")

    # 3. Configure Public Hostname
    # This involves updating the tunnel configuration
    print(f"[*] Configuring Public Hostname: {SUBDOMAIN}.{DOMAIN} -> {TARGET_SERVICE}...")
    
    # First, get existing config to not overwrite other hostnames if any
    resp = requests.get(f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations", headers=headers)
    
    config = {}
    if resp.status_code == 200:
        config = resp.json().get("result", {}).get("config", {})
    
    ingress = config.get("ingress", [])
    
    # Remove the default 404 if it exists to add our new rule before it
    ingress = [rule for rule in ingress if rule.get("service") != "http_status:404"]
    
    # Add our rule
    new_rule = {
        "hostname": f"{SUBDOMAIN}.{DOMAIN}",
        "service": TARGET_SERVICE
    }
    
    # Avoid duplicates
    if not any(rule.get("hostname") == new_rule["hostname"] for rule in ingress):
        ingress.append(new_rule)
    
    # Add back the default 404 at the end
    ingress.append({"service": "http_status:404"})
    
    payload = {
        "config": {
            "ingress": ingress
        }
    }
    
    resp = requests.put(f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations", headers=headers, json=payload)
    
    if resp.status_code == 200:
        print(f"[+] Successfully configured routing for {SUBDOMAIN}.{DOMAIN}")
    else:
        print(f"[-] Failed to configure routing: {resp.text}")

    # 4. Create DNS Record (optional but usually needed)
    print(f"[*] Checking DNS record for {SUBDOMAIN}.{DOMAIN}...")
    # Need Zone ID first
    resp = requests.get(f"https://api.cloudflare.com/client/v4/zones?name={DOMAIN}", headers=headers)
    zones = resp.json().get("result", [])
    if not zones:
        print(f"[-] Could not find Zone ID for {DOMAIN}. Please ensure the domain is in your Cloudflare account.")
        return
    
    zone_id = zones[0]["id"]
    
    # Create CNAME record pointing to <tunnel_id>.cfargotunnel.com
    dns_payload = {
        "type": "CNAME",
        "name": SUBDOMAIN,
        "content": f"{tunnel_id}.cfargotunnel.com",
        "proxied": True
    }
    
    resp = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", headers=headers, json=dns_payload)
    if resp.status_code == 200:
        print(f"[+] DNS CNAME record created for {SUBDOMAIN}.{DOMAIN}")
    elif "already exists" in resp.text:
        print(f"[!] DNS record already exists, skipping.")
    else:
        print(f"[-] Failed to create DNS record: {resp.text}")

if __name__ == "__main__":
    setup_cloudflare()
