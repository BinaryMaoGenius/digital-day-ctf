import tornado.options
from tornado.options import options
import rootthebox # This defines the options
tornado.options.parse_command_line(args=['--config=files/rootthebox.cfg'])

from models import dbsession
from models.User import User

# Mocking options if needed, but models usually handle defaults
try:
    admin = User.by_handle("admin")
    if admin:
        admin.password = "rootthebox"
        dbsession.add(admin)
        dbsession.commit()
        print("Password for 'admin' reset to 'rootthebox'")
    else:
        print("User 'admin' not found.")
except Exception as e:
    print(f"Error: {e}")
