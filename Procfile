web:
    gunicorn src_fun_fact.wsgi
    python src/manage.py test --liveserver=0.0.0.0:$PORT
release: python manage.py migrate
