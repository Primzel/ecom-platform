#!/usr/bin/env bash
source .env/bin/activate

export DJANGO_SETTINGS_MODULE=e_store_primzel.settings
export PRIMZEL_DEBUG=False
export POSTGRES_HOST=primzel-demo-rds.c2irzwqclpkg.us-east-2.rds.amazonaws.com
export POSTGRES_USER=primzel
export POSTGRES_PASSWORD=Primzel44332211