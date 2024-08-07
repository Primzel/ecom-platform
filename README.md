# README - Project Setup Instructions

![Migration Checker](https://github.com/Primzel/ecom-platform/actions/workflows/migrations-checker.yml/badge.svg)

## SSL Setup

Follow the instructions [here](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal) to set up SSL.

## Environment Setup

1. Create a virtual environment: `virtualenv -p <python-path> .env`
2. Activate the virtual environment: `source path-to-env-activate`
3. Install dependencies: `pip install -r requirements.txt`

## Database Schema Creation

1. Generate migrations: `python manage.py makemigrations`
2. Apply migrations: `python manage.py migrate`

## Running Tests

Execute tests using: `python manage.py test`

## Country Setup

Populate country data: `python manage.py oscar_populate_countries`

## Superuser Creation

Create a superuser account: `python manage.py createsuperuser`

## Stripe CLI Integration

Replace `<paste-api-key-here>` with your actual Stripe API key.

1. `docker run --rm -it stripe/stripe-cli listen --load-from-webhooks-api --forward-to 192.168.1.4:8000 --api-key <paste-api-key-here>`
2. `docker run --rm -it stripe/stripe-cli logs tail --api-key <paste-api-key-here>`
3. `docker run --rm -it stripe/stripe-cli trigger charge.succeeded --api-key <paste-api-key-here>`

## Server Setup Steps

### Environment Variables

Set the following environment variables:

```shell
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=e_store_primzel.settings
export POSTGRES_HOST=localhost
export PRIMZEL_DEBUG=True
```

### Configuration in Local Settings

Add the following parameters in `/web-backend/e_store_primzel/settings/env/local.py`:

```python
THUMBNAIL_DEBUG = True
THUMBNAIL_PRESERVE_FORMAT = True
```

### Creating a Tenant

- Schema: eggs
- Command: `./manage.py create_tenant`

### AWS CLI Installation

1. Download and install AWS CLI:
   ```shell
   curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
   unzip awscli-bundle.zip
   sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
   ```
2. Create S3 Bucket
   ```shell
   aws --endpoint-url=http://localhost:4566 s3 mb s3://demo-bucket
   ```

### Importing Data to Local S3

-
Command: `./manage.py tenant_command import_from_woocommerce --schema=eggs "http://www.website.com" "ck_*****" "cs_*****"`

## Service Creation on Server

1. Add `store.oscar.com` to `/etc/hosts`.
2. Create a systemd service file: `/etc/systemd/system/primzel-backend.service`.
3. Populate the file with the following configuration, replacing sensitive data with your actual credentials.
   ```shell
   [Unit]
   Description=Primzel backend.

   [Service]
   # Environment variables with masked sensitive data
   Environment="POSTGRES_PASSWORD=********"
   Environment="AWS_ACCESS_KEY_ID=********"
   Environment="AWS_SECRET_ACCESS_KEY=********"
   # Additional configurations...

   WorkingDirectory=/home/ec2-user/codebase/web-backend
   ExecStart=/home/ec2-user/codebase/web-backend/.env/bin/gunicorn --workers 8 --bind 0.0.0.0:8080 e_store_primzel.wsgi:application --chdir /home/ec2-user/codebase/web-backend
   ```

## Nginx Configuration

1. Create an Nginx configuration file: `/etc/nginx/conf.d/demo.primzel.com.conf`.
2. Add the following server block configuration:
   ```nginx
   server {
       server_name demo.primzel.com;
       listen 443;

       ssl on;
       ssl_certificate /etc/ssl/demo.primzel.com/certificate.crt;
       ssl_certificate_key /etc/ssl/demo.primzel.com/private.key;

       # Additional Nginx configurations...
   }
   ```
