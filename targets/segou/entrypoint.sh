#!/bin/sh
python -c "from app import init_db; init_db()"
exec gunicorn -k gevent -w 4 -b 0.0.0.0:8001 app:app
