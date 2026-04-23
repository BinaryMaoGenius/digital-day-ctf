import os
import sys
# Add current dir to sys.path
sys.path.append(os.getcwd())

import tornado.options
from tornado.options import options
import rootthebox
# Parse config
options.parse_command_line(args=['--config=files/rootthebox.cfg', '--sql_dialect=sqlite', '--sql_database=files/rootthebox.db'])

from models import dbsession
from models.User import User
from models.Permission import Permission
from models.User import ADMIN_PERMISSION

try:
    user = User.by_handle("admin")
    if not user:
        print("Creating admin user...")
        user = User(handle="admin")
        dbsession.add(user)
        dbsession.flush()

    user.password = "rootthebox"
    dbsession.add(user)
    dbsession.flush()

    # Grant admin if not already
    if ADMIN_PERMISSION not in user.permissions_names:
        print("Granting admin permissions...")
        perm = Permission(name=ADMIN_PERMISSION, user_id=user.id)
        dbsession.add(perm)

    dbsession.commit()
    print("SUCCESS: Admin password reset to 'rootthebox'")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
