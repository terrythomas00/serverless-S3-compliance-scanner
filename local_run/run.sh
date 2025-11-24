#!/usr/bin/env bash
# Uses your local AWS creds via env or volume mount

#export DOCKER_BUILDKIT=1

#docker build -t s3-scanner-local -f ./local_run/Dockerfile .
docker run --rm \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN \
  -e AWS_REGION=us-east-1 \
  -e REPORTS_BUCKET="$REPORTS_BUCKET" \
  s3-scanner-local
