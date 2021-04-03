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
./manage.py tenant_command import_from_woocommerce --schema=eggs "http://www.hoko.pk" "ck_5370bb23c2327f912da64abf4ced3e0c5c8363d2" "cs_cbdd51bafd47fa9356401f09fa321e0f95080f7e"

# How to create service on server.
1. add `store.oscar.com` in `/etc/hosts`
2. create file `/etc/systemd/system/primzel-backend.service`
3. add below content in the file.
```
[Unit]
Description=Primzel backend.

[Service]
User=ec2-user
Group=nginx
Environment="DJANGO_SETTINGS_MODULE=e_store_primzel.settings"
Environment="PRIMZEL_DEBUG=False"
Environment="POSTGRES_HOST=primzel-demo-rds.c2irzwqclpkg.us-east-2.rds.amazonaws.com"
Environment="POSTGRES_USER=primzel"
Environment="POSTGRES_PASSWORD=Primzel44332211"
Environment="AWS_ACCESS_KEY_ID=AKIAJLCUH4TDT3G4ORYQ"
Environment="AWS_SECRET_ACCESS_KEY=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"
Environment="AWS_STORAGE_BUCKET_NAME=primzel-demo"
Environment="AWS_S3_ENDPOINT_URL=https://primzel-demo.s3.us-east-2.amazonaws.com/"
Environment="AWS_SES_REGION_NAME=us-east-2"
Environment="AWS_SES_REGION_ENDPOINT=email.us-east-2.amazonaws.com"
Environment="CELERY_BROKER_URL=redis://demo-redis-server.awwrga.ng.0001.use2.cache.amazonaws.com:6379"
Environment="CELERY_RESULT_BACKEND=redis://demo-redis-server.awwrga.ng.0001.use2.cache.amazonaws.com:6379/0"
Environment="DJANGO_LOG_LEVEL=INFO"
Environment="EMAIL_BACKEND=django_ses.SESBackend"


WorkingDirectory=/home/ec2-user/codebase/web-backend
ExecStart=/home/ec2-user/codebase/web-backend/.env/bin/gunicorn --workers 8 --bind 0.0.0.0:8080  e_store_primzel.wsgi:application --chdir /home/ec2-user/codebase/web-backend --log-file /var/log/primzel-backend/general.log --error-logfile /var/log/primzel-backend/errors.log --log-level debug
```

# How to configure with nginx
1. create nginx site configuration file `/etc/nginx/conf.d/demo.primzel.com.conf`
2. add below content in the the.
```
server {
    server_name demo.primzel.com;
    listen   443;
    
    ssl    on;
    ssl_certificate    /etc/ssl/demo.primzel.com/certificate.crt; 
    ssl_certificate_key    /etc/ssl/demo.primzel.com/private.key;

    location / {
        proxy_pass http://store.oscar.com:8080;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
	#include uwsgi_params;
	#uwsgi_pass http://unix:/home/ec2-user/codebase/web-backend/backend.sock;
    }
    location /static/ {
        alias /home/ec2-user/codebase/web-backend/staticfiles/eggs/;
        autoindex off;
    }
}
```