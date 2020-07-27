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

#Stripe Cli.

1. docker run --rm -it stripe/stripe-cli listen --load-from-webhooks-api --forward-to 192.168.1.4:8000 --api-key <paste-api-key-here>
2. docker run --rm -it stripe/stripe-cli logs tail --api-key <paste-api-key-here>
3. docker run --rm -it stripe/stripe-cli trigger charge.succeeded --api-key <paste-api-key-here>

### Steps need to run server
Set following enviorment variables 
export PYTHONUNBUFFERED=1 && export DJANGO_SETTINGS_MODULE=e_store_primzel.settings && export POSTGRES_HOST=localhost && export PRIMZEL_DEBUG=True

Add following parameters in /web-backend/e_staore_primzel/settings/env/lcoal.py
THUMBNAIL_DEBUG = True 
THUMBNAIL_PRESERVE_FORMAT = True


Create tenant
schema: eggs
./manage.py create_tenant


Install AWS CLI
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

aws --endpoint-url=http://localhost:4572 s3 mb s3://demo-bucket

Import data to local S3
./manage.py tenant_command import_from_woocommerce --schema=eggs "http://www.hoko.pk" "ck_5370bb23c2327f912da64abf4ced3e0c5c8363d2" “cs_cbdd51bafd47fa9356401f09fa321e0f95080f7e”