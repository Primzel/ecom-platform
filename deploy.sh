#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CFN_DIR="$SCRIPT_DIR/cloudformation"

usage() {
  echo "Usage: $0 <env> [options]"
  echo ""
  echo "  env         dev | stage | production"
  echo ""
  echo "Options:"
  echo "  --tag <tag>           Image tag to deploy (default: last built tag or <version>-<git-sha>)"
  echo "  --stack <target>      infra | app | all  (default: all)"
  echo "  --run-migrations      Run 'manage.py migrate_schemas' as a one-off ECS task"
  echo "  --create-db           Create the primzel_store database on RDS (run once after infra deploy)"
  echo "  --dry-run             Print commands without executing"
  echo ""
  echo "Examples:"
  echo "  $0 dev --stack all --create-db --run-migrations   # First-time full deploy"
  echo "  $0 production --stack app --tag abc1234 --run-migrations"
  exit 1
}

[[ $# -lt 1 ]] && usage

ENV="$1"; shift
IMAGE_TAG=""
STACK_TARGET="all"
RUN_MIGRATIONS=false
CREATE_DB=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --tag)              IMAGE_TAG="$2"; shift 2 ;;
    --stack)            STACK_TARGET="$2"; shift 2 ;;
    --run-migrations)   RUN_MIGRATIONS=true; shift ;;
    --create-db)        CREATE_DB=true; shift ;;
    --dry-run)          DRY_RUN=true; shift ;;
    -h|--help)          usage ;;
    *)                  echo "ERROR: Unknown option: $1"; usage ;;
  esac
done

case "$ENV" in
  dev|stage|production) ;;
  *) echo "ERROR: env must be dev, stage, or production"; usage ;;
esac

case "$STACK_TARGET" in
  infra|app|all) ;;
  *) echo "ERROR: --stack must be infra, app, or all"; exit 1 ;;
esac

# --- resolve version and image tag
VERSION="$(tr -d '[:space:]' < "$SCRIPT_DIR/VERSION")"
GIT_SHA="$(git rev-parse --short HEAD)"

if [[ -z "$IMAGE_TAG" ]]; then
  if [[ -f "$SCRIPT_DIR/.last-build-tag" ]]; then
    IMAGE_TAG="$(cat "$SCRIPT_DIR/.last-build-tag")"
    echo "==> Using last build tag: $IMAGE_TAG"
  else
    IMAGE_TAG="${VERSION}-${GIT_SHA}"
    echo "WARN: No --tag provided and no .last-build-tag found, falling back to '${IMAGE_TAG}'"
  fi
fi

# --- config
AWS_REGION="us-east-2"
AWS_ACCOUNT_ID="262004543713"
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/primzel-ecom-${ENV}"

INFRA_STACK="primzel-ecom-infra-${ENV}"
APP_STACK="primzel-ecom-app-${ENV}"

echo ""
echo "==> Deploy configuration"
echo "    Environment  : $ENV"
echo "    Version      : $VERSION"
echo "    Region       : $AWS_REGION"
echo "    Account      : $AWS_ACCOUNT_ID"
echo "    Image        : ${ECR_URI}:${IMAGE_TAG}"
echo "    Stack target : $STACK_TARGET"
[[ "$DRY_RUN" == "true" ]] && echo "    Mode         : DRY RUN (no changes will be applied)"
echo ""

# --- helpers

run() {
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] $*"
  else
    "$@"
  fi
}

# Build --parameter-overrides array from a JSON file (flat key-value object)
# JSON format: { "Key": "value", ... }
build_overrides() {
  local params_file="$1"
  shift
  # Additional key=value pairs passed as arguments are appended
  local overrides=()
  while IFS="=" read -r key value; do
    overrides+=("${key}=${value}")
  done < <(jq -r 'to_entries | .[] | "\(.key)=\(.value)"' "$params_file")
  for extra in "$@"; do
    overrides+=("$extra")
  done
  printf '%s\n' "${overrides[@]}"
}

deploy_stack() {
  local stack_name="$1"
  local template="$2"
  local params_file="$3"
  shift 3
  # Any remaining args are extra Key=Value overrides
  local extra_overrides=("$@")

  echo "==> Deploying stack: $stack_name"
  echo "    Template : $template"
  echo "    Params   : $params_file"

  if [[ ! -f "$params_file" ]]; then
    echo "ERROR: Parameters file not found: $params_file"
    exit 1
  fi

  local overrides=()
  while IFS= read -r line; do
    overrides+=("$line")
  done < <(build_overrides "$params_file" "${extra_overrides[@]+"${extra_overrides[@]}"}")

  run aws cloudformation deploy \
    --stack-name "$stack_name" \
    --template-file "$template" \
    --parameter-overrides "${overrides[@]}" \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
    --region "$AWS_REGION" \
    --no-fail-on-empty-changeset

  echo "    Done: $stack_name"
}

stack_output() {
  local stack_name="$1"
  local output_key="$2"
  aws cloudformation describe-stacks \
    --stack-name "$stack_name" \
    --query "Stacks[0].Outputs[?OutputKey=='${output_key}'].OutputValue" \
    --output text \
    --region "$AWS_REGION"
}

# --- deploy functions

deploy_infra() {
  deploy_stack \
    "$INFRA_STACK" \
    "$CFN_DIR/infrastructure.yml" \
    "$CFN_DIR/parameters/${ENV}/infra.json"
}

deploy_app() {
  deploy_stack \
    "$APP_STACK" \
    "$CFN_DIR/service.yml" \
    "$CFN_DIR/parameters/${ENV}/service.json" \
    "ImageUri=${ECR_URI}:${IMAGE_TAG}" \
    "InfraStackName=${INFRA_STACK}"
}

create_db() {
  echo ""
  echo "==> Creating database 'primzel_store' on RDS..."

  local cluster subnet sg task_def task_arn exit_code

  cluster="$(stack_output "$INFRA_STACK" ECSClusterName)"
  subnet="$(stack_output "$INFRA_STACK" PrivateSubnet1)"
  sg="$(stack_output "$INFRA_STACK" ECSSecurityGroup)"
  task_def="primzel-${ENV}-web"

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] aws ecs run-task --cluster $cluster --task-definition $task_def --overrides '{...CREATE DATABASE primzel_store...}'"
    return
  fi

  task_arn="$(aws ecs run-task \
    --cluster "$cluster" \
    --task-definition "$task_def" \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$subnet],securityGroups=[$sg],assignPublicIp=DISABLED}" \
    --overrides '{
      "containerOverrides": [{
        "name": "web",
        "command": [
          "bash", "-c",
          "PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -c \"SELECT 1 FROM pg_database WHERE datname='\''primzel_store'\''\" | grep -q 1 && echo \"Database already exists\" || PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -c \"CREATE DATABASE primzel_store\""
        ]
      }]
    }' \
    --region "$AWS_REGION" \
    --query 'tasks[0].taskArn' \
    --output text)"

  echo "    Task ARN : $task_arn"
  echo "    Waiting for create-db task to complete..."

  aws ecs wait tasks-stopped \
    --cluster "$cluster" \
    --tasks "$task_arn" \
    --region "$AWS_REGION"

  exit_code="$(aws ecs describe-tasks \
    --cluster "$cluster" \
    --tasks "$task_arn" \
    --region "$AWS_REGION" \
    --query 'tasks[0].containers[0].exitCode' \
    --output text)"

  if [[ "$exit_code" != "0" ]]; then
    echo "ERROR: create-db task failed with exit code $exit_code"
    echo "       Check CloudWatch logs at /primzel/${ENV}/web"
    exit 1
  fi

  echo "    Database 'primzel_store' is ready."
}

run_migrations() {
  echo ""
  echo "==> Running migrations (migrate_schemas) as one-off ECS task..."

  local cluster subnet sg task_def task_arn exit_code

  cluster="$(stack_output "$INFRA_STACK" ECSClusterName)"
  subnet="$(stack_output "$INFRA_STACK" PrivateSubnet1)"
  sg="$(stack_output "$INFRA_STACK" ECSSecurityGroup)"
  task_def="primzel-${ENV}-web"

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY RUN] aws ecs run-task --cluster $cluster --task-definition $task_def --overrides '{...migrate_schemas...}'"
    return
  fi

  task_arn="$(aws ecs run-task \
    --cluster "$cluster" \
    --task-definition "$task_def" \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$subnet],securityGroups=[$sg],assignPublicIp=DISABLED}" \
    --overrides '{
      "containerOverrides": [{
        "name": "web",
        "command": ["python", "manage.py", "migrate_schemas", "--noinput"]
      }]
    }' \
    --region "$AWS_REGION" \
    --query 'tasks[0].taskArn' \
    --output text)"

  echo "    Task ARN : $task_arn"
  echo "    Waiting for migration task to complete..."

  aws ecs wait tasks-stopped \
    --cluster "$cluster" \
    --tasks "$task_arn" \
    --region "$AWS_REGION"

  exit_code="$(aws ecs describe-tasks \
    --cluster "$cluster" \
    --tasks "$task_arn" \
    --region "$AWS_REGION" \
    --query 'tasks[0].containers[0].exitCode' \
    --output text)"

  if [[ "$exit_code" != "0" ]]; then
    echo "ERROR: Migration task failed with exit code $exit_code"
    echo "       Check CloudWatch logs at /primzel/${ENV}/web"
    exit 1
  fi

  echo "    Migrations completed successfully."
}

wait_for_service() {
  local cluster="$1"
  local service="$2"
  echo ""
  echo "==> Waiting for service to stabilize: $service"
  aws ecs wait services-stable \
    --cluster "$cluster" \
    --services "$service" \
    --region "$AWS_REGION"
}

# --- main

case "$STACK_TARGET" in
  infra)
    deploy_infra
    ;;
  app)
    deploy_app
    [[ "$CREATE_DB" == "true" ]] && create_db
    [[ "$RUN_MIGRATIONS" == "true" ]] && run_migrations
    ;;
  all)
    deploy_infra
    deploy_app
    [[ "$CREATE_DB" == "true" ]] && create_db
    [[ "$RUN_MIGRATIONS" == "true" ]] && run_migrations
    ;;
esac

if [[ "$STACK_TARGET" != "infra" && "$DRY_RUN" != "true" ]]; then
  CLUSTER="$(stack_output "$INFRA_STACK" ECSClusterName)"
  WEB_SVC="$(stack_output "$APP_STACK" WebServiceName)"
  wait_for_service "$CLUSTER" "$WEB_SVC"

  ALB_DNS="$(stack_output "$INFRA_STACK" LoadBalancerDNS)"
  echo ""
  echo "==> Deployment complete!"
  echo "    URL : http://${ALB_DNS}"
fi
