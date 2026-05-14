#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  echo "Usage: $0 <env> [options]"
  echo ""
  echo "  env         dev | stage | production"
  echo ""
  echo "Options:"
  echo "  --push          Push image to ECR after building"
  echo "  --tag <tag>     Custom image tag (default: <version>-<git-sha> from VERSION file)"
  echo "  --no-cache      Build without Docker layer cache"
  echo ""
  echo "Examples:"
  echo "  $0 dev --push"
  echo "  $0 production --push --tag v1.2.3"
  exit 1
}

[[ $# -lt 1 ]] && usage

ENV="$1"; shift
PUSH=false
CUSTOM_TAG=""
NO_CACHE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --push)      PUSH=true; shift ;;
    --tag)       CUSTOM_TAG="$2"; shift 2 ;;
    --no-cache)  NO_CACHE="--no-cache"; shift ;;
    -h|--help)   usage ;;
    *)           echo "ERROR: Unknown option: $1"; usage ;;
  esac
done

case "$ENV" in
  dev|stage|production) ;;
  *) echo "ERROR: env must be dev, stage, or production"; usage ;;
esac

AWS_REGION="us-east-2"
AWS_ACCOUNT_ID="262004543713"
ECR_REPO="primzel-ecom-${ENV}"
ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

GIT_SHA="$(git rev-parse --short HEAD)"
VERSION="$(tr -d '[:space:]' < "$SCRIPT_DIR/VERSION")"
IMAGE_TAG="${CUSTOM_TAG:-${VERSION}-${GIT_SHA}}"
# Env-scoped latest so dev and production don't collide
ENV_LATEST="${ENV}-latest"

echo "==> Building for environment : $ENV"
echo "    Version   : $VERSION"
echo "    ECR URI   : $ECR_URI"
echo "    Image tag : $IMAGE_TAG"
echo "    Platform  : linux/amd64"

docker build \
  ${NO_CACHE} \
  --platform linux/amd64 \
  --build-arg BUILD_ENV="$ENV" \
  --build-arg GIT_SHA="$GIT_SHA" \
  --build-arg VERSION="$VERSION" \
  --provenance=false \
  -t "${ECR_REPO}:${IMAGE_TAG}" \
  -t "${ECR_REPO}:${ENV_LATEST}" \
  "$SCRIPT_DIR"

echo "==> Build complete: ${ECR_REPO}:${IMAGE_TAG}"

if [[ "$PUSH" == "true" ]]; then
  echo ""
  echo "==> Authenticating to ECR..."
  aws ecr get-login-password --region "$AWS_REGION" \
    | docker login --username AWS --password-stdin \
        "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

  # Create the ECR repo if it doesn't exist yet
  if ! aws ecr describe-repositories \
        --repository-names "$ECR_REPO" \
        --region "$AWS_REGION" &>/dev/null; then
    echo "==> Creating ECR repository: $ECR_REPO"
    aws ecr create-repository \
      --repository-name "$ECR_REPO" \
      --region "$AWS_REGION" \
      --image-scanning-configuration scanOnPush=true \
      --encryption-configuration encryptionType=AES256 \
      > /dev/null
  fi

  echo "==> Pushing to ECR..."
  docker tag "${ECR_REPO}:${IMAGE_TAG}" "${ECR_URI}:${IMAGE_TAG}"
  docker tag "${ECR_REPO}:${IMAGE_TAG}" "${ECR_URI}:${ENV_LATEST}"

  docker push "${ECR_URI}:${IMAGE_TAG}"
  docker push "${ECR_URI}:${ENV_LATEST}"

  echo "==> Pushed:"
  echo "    ${ECR_URI}:${IMAGE_TAG}"
  echo "    ${ECR_URI}:${ENV_LATEST}"

  # Persist tag so deploy.sh can pick it up automatically
  echo "$IMAGE_TAG" > "$SCRIPT_DIR/.last-build-tag"
fi
