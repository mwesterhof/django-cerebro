# django cerebro - scikit-based machine learning over REST API

## installation
1. create and activate virtual environment through manager of your choosing
2. make install
3. (optionally) create superuser


## how to use
- run application through './manage.py runserver' or 'make uwsgi'
- Use /register/ endpoint to enter measured conversion data for a visitor, and to view existing data
- User /predict/ endpoint to enter measured stats for a visitor and ask for conversion predictions

When running the application through './manage.py runserver', it's necessary to manually retrain the neural net using
'./manage.py train_net' in order to see changed results. When using 'make uwsgi', the net is automatically retrained
every minute
