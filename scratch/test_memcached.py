import memcache
from tornado.options import options, define

# Define options so we can read the config
if 'memcached' not in options:
    define("memcached", default="127.0.0.1:11211")
if 'memcached_user' not in options:
    define("memcached_user", default="")
if 'memcached_password' not in options:
    define("memcached_password", default="")

try:
    options.parse_config_file("files/rootthebox.cfg")
except:
    pass

print(f"Connecting to: {options.memcached}")
client = memcache.Client(options.memcached.split(","), debug=1)
stats = client.get_stats()
print(f"Stats: {stats}")

if not stats:
    print("FAILED: No memcached server found!")
else:
    print("SUCCESS: Memcached is running.")
    client.set("test_key", "hello")
    print(f"Test Get: {client.get('test_key')}")
