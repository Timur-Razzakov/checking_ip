# gunicorn -c etc/gunicorn/gunicorn_config.py checking.wsgi


command = '/root/checking_ip/venv/bin/gunicorn'
pythonpath = '/root/checking_ip'
bind = '193.200.16.197:8000'
workers = 3
