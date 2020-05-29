#!/usr/bin/env bash
source .env/bin/activate

export DJANGO_SETTINGS_MODULE=e_store_primzel.settings
export PRIMZEL_DEBUG=True
export POSTGRES_HOST=localhost
export POSTGRES_USER=primzel_store
export POSTGRES_PASSWORD=primzel_store
#export AWS_ACCESS_KEY_ID=123
#export AWS_SECRET_ACCESS_KEY=123
#export AWS_STORAGE_BUCKET_NAME=primzel-demo
#export AWS_S3_ENDPOINT_URL=https://primzel-demo.s3.us-east-2.amazonaws.com/