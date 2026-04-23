
import os
from tornado.options import options, define
from models import dbsession
from models.Box import Box

# Define necessary options to avoid AttributeError
if 'log-sql' not in options:
    define("log-sql", default=False, type=bool)
if 'sql-dialect' not in options:
    define("sql-dialect", default="sqlite")
if 'sql-database' not in options:
    define("sql-database", default="files/rootthebox.db")

# Fake config parsing to initialize
options.sql_database = "files/rootthebox.db"

try:
    boxes = Box.all()
    for b in boxes:
        print(f"{b.name} === {b.uuid}")
except Exception as e:
    print(f"Error: {e}")
