#!/bin/bash
# build image 

image="opencode-agent"

set -xe

cd "$(dirname $0)"

python generate_models_config.py

docker build --no-cache "$@" -t $image:latest -f Dockerfile .

docker builder prune -f
docker images | grep $image

