# Primzel E-Commerce Platform

![Migration Checker](https://github.com/Primzel/ecom-platform/actions/workflows/migrations-checker.yml/badge.svg)

Django + django-oscar multi-tenant e-commerce platform deployed on AWS ECS Fargate.

---

## Local Development

### Prerequisites

- Docker & Docker Compose
- Python 3.x + virtualenv

### Setup

```shell
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements
```

### Run locally

```shell
docker-compose up
```

Services started: Django (gunicorn), PostgreSQL, Redis, LocalStack S3, Stripe CLI.

### Useful make commands

```shell
make dev.migrate                          # Run migrate_schemas
make dev.makemigrations                   # Generate migrations
make dev.collectstatic schema=<schema>    # Collect static files
make dev.create_superuser email=<email> schema=<schema>
make dev.web.shell                        # Shell into web container
make dev.postgres.shell                   # psql shell
```

---

## AWS Deployment

### Prerequisites

- AWS CLI configured with sufficient IAM permissions (see below)
- Docker with `linux/amd64` build support
- `jq` installed

### Repository / file structure

```
build.sh                                  # Build and push Docker image to ECR
deploy.sh                                 # Deploy CloudFormation stacks
VERSION                                   # Current version (e.g. 0.1.1)
cloudformation/
  infrastructure.yml                      # VPC, RDS (optional), Redis, ALB, ECS cluster, IAM
  task-definitions.yml                    # ECS task definitions (web, celery-worker, celery-beat)
  service.yml                             # ECS services and auto-scaling
  parameters/
    dev/infra.json                         # Dev infrastructure parameters
    dev/task-definitions.json             # Dev task sizing parameters
    dev/service.json                       # Dev service scaling parameters
    stage/infra.json
    stage/task-definitions.json
    stage/service.json
    production/infra.json
    production/task-definitions.json
    production/service.json
```

Stacks are deployed in order: `infra` → `task-definitions` → migrations → `service`. This guarantees migrations run against the new image before any traffic-serving tasks start.

### Environment differences

| | dev | stage | production |
|---|---|---|---|
| RDS | external (via `ExistingDBEndpoint`) | external (via `ExistingDBEndpoint`) | t3.medium, Multi-AZ, provisioned |
| Redis | t3.micro, single node | t3.small, single node | t3.medium, primary + replica |
| NAT Gateway | 1 | 1 | 1 per AZ |
| Fargate capacity | SPOT | SPOT | on-demand |
| Web tasks | 0 min / 1 max | 1 min / 3 max | 2 min / 10 max |
| Gunicorn workers | 2 | 2 | 4 |

### Database configuration

RDS is only provisioned for production by default. For dev and stage, point the deployment at an existing PostgreSQL instance:

**`cloudformation/parameters/dev/infra.json`**
```json
{
  "ExistingDBEndpoint": "my-postgres.example.com",
  "ExistingDBSecretArn": "arn:aws:secretsmanager:us-east-2:ACCOUNT:secret/my-db-secret"
}
```

The secret must have `username` and `password` keys. For dev you can create a Secrets Manager secret manually and paste the ARN here.

To provision RDS for dev or stage (e.g. for a more production-like test), pass `--force-rds`:

```shell
./deploy.sh stage --stack infra --force-rds
```

### build.sh

Builds the Docker image and optionally pushes to ECR. The default tag is `<version>-<git-sha>` derived from the `VERSION` file and current commit.

```shell
./build.sh <env> [--push] [--tag <tag>] [--no-cache]

# Examples
./build.sh dev --push
./build.sh production --push --tag v1.2.0
```

After a successful push the tag is saved to `.last-build-tag` and picked up automatically by `deploy.sh`.

### deploy.sh

Deploys or updates CloudFormation stacks.

```shell
./deploy.sh <env> [options]
```

| Flag | Description |
|---|---|
| `--stack infra` | Deploy VPC / RDS / Redis / ALB / ECS cluster only |
| `--stack app` | Deploy task definitions and services only |
| `--stack all` | Deploy both (default) |
| `--tag <tag>` | Image tag to deploy (defaults to `.last-build-tag` or `<version>-<git-sha>`) |
| `--create-db` | Create the `primzel_store` database on RDS (run once after first infra deploy) |
| `--run-migrations` | Run `manage.py migrate_schemas` as a one-off ECS task before services start |
| `--force-rds` | Provision an RDS instance even for dev/stage |
| `--dry-run` | Print all commands without executing |

### First-time environment setup

```shell
# 1. Build and push the image
./build.sh dev --push

# 2. Deploy infrastructure + app, create the database, and run migrations
./deploy.sh dev --stack all --create-db --run-migrations
```

For dev/stage, set `ExistingDBEndpoint` and `ExistingDBSecretArn` in `cloudformation/parameters/dev/infra.json` before step 2.

For production (RDS is provisioned automatically):

```shell
./build.sh production --push
./deploy.sh production --stack all --create-db --run-migrations
```

### Subsequent deploys

```shell
./build.sh production --push
./deploy.sh production --stack app --run-migrations
```

### Updating infrastructure only (e.g. resize DB)

```shell
./deploy.sh production --stack infra
```

### Before deploying to production

1. Replace `REPLACE_ME` in `cloudformation/parameters/production/infra.json` with a valid ACM certificate ARN.
2. Create the S3 media buckets: `primzel-dev-media`, `primzel-stage-media`, `primzel-production-media`.

### Required IAM permissions

The deploying user/role needs permissions across: CloudFormation, ECR, EC2, ELB, ECS, IAM, RDS, Secrets Manager, ElastiCache, CloudWatch Logs, and Application Auto Scaling. See the full permission list in the project wiki or ask the platform team.

---

## Versioning

The `VERSION` file at the repo root is the single source of truth for the release version.

```shell
echo "1.2.0" > VERSION
git commit -m "chore: bump version to 1.2.0" VERSION
./build.sh production --push          # tags image as 1.2.0-<sha>
./deploy.sh production --stack app --run-migrations
```

---

## Celery

Background tasks run as separate ECS services (`celery-worker`, `celery-beat`) using the same Docker image as the web service.

- Worker queue: `celery_app`
- Broker / result backend: ElastiCache Redis over TLS (`rediss://`)
- Beat scheduler: default (override with `DatabaseScheduler` if `django-celery-beat` is installed)

---

## Tenant management

```shell
# Create a new tenant (run inside the web container or via ECS exec)
python manage.py create_tenant

# Populate countries for a tenant
python manage.py tenant_command oscar_populate_countries --schema=<schema>

# Import products from WooCommerce
python manage.py tenant_command import_from_woocommerce --schema=<schema> "<host>" "<ck_key>" "<cs_key>"
```

---

## Stripe CLI (local testing)

```shell
docker run --rm -it stripe/stripe-cli listen \
  --load-from-webhooks-api \
  --forward-to 192.168.1.4:8000 \
  --api-key <stripe-api-key>
```
