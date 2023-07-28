uwsgi: collectstatic
	uwsgi --ini uwsgi.ini

collectstatic:
	./manage.py collectstatic --noinput

install:
	pip install -r requirements.txt
	./manage.py migrate
	-mkdir -p cerebro/media
