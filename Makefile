uwsgi: collectstatic
	uwsgi --ini uwsgi.ini

collectstatic:
	./manage.py collectstatic --noinput
