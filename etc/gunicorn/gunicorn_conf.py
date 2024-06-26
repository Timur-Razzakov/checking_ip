# gunicorn -c etc/gunicorn/gunicorn_config.py checking.wsgi


command = '/root/checking_ip/venv/bin/gunicorn'
pythonpath = '/root/checking_ip'
bind = '143.47.224.206'
workers = 3
