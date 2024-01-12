#!/usr/bin/env bash
source .env/bin/activate

export DJANGO_SETTINGS_MODULE=e_store_primzel.settings
export PRIMZEL_DEBUG=False
export POSTGRES_HOST=primzel-prod.us-east-2.rds.amazonaws.com
export POSTGRES_USER=primzel
export POSTGRES_PASSWORD=Primzel
export AWS_ACCESS_KEY_ID=*******
export AWS_SECRET_ACCESS_KEY=*******
export AWS_STORAGE_BUCKET_NAME=primzel-prod-shared
export AWS_S3_ENDPOINT_URL=https://bucket-shared.s3.us-east-2.amazonaws.com/
export POSTGRES_DB_NAME=primzel-production
