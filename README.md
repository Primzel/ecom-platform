#How to setup environment.

1. `virtualenv -p <python-path> .env`
2. `source path-to-env-activate`
3. pip install -r requirements

# How to create database schema.
1. `python manage.py makemigrations`
2. `python manage.py migrate`

# How to start test.
1. `python manage.py test`

#How to setup countries.
1. `python manage.py oscar_populate_countries`

#How to create superuser.

1. `python manage.py createsuperuser`