#!/usr/bin/env bash
source .env/bin/activate

export DJANGO_SETTINGS_MODULE=e_store_primzel.settings
export PRIMZEL_DEBUG=False
export POSTGRES_HOST=primzel-demo-rds.c2irzwqclpkg.us-east-2.rds.amazonaws.com
export POSTGRES_USER=primzel
export POSTGRES_PASSWORD=Primzel44332211
export AWS_ACCESS_KEY_ID=AKIAJLCUH4TDT3G4ORYQ
export AWS_SECRET_ACCESS_KEY=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
export AWS_STORAGE_BUCKET_NAME=primzel-demo
export AWS_S3_ENDPOINT_URL=https://primzel-demo.s3.us-east-2.amazonaws.com/