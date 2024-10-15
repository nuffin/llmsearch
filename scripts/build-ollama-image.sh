#!/usr/bin/env bash

set -x

IMAGE_NAME="ollama"

TAG="${IMAGE_NAME}:$(date +%m%d_%H%M)"

TAG_SUFFIX=$1
test ! -z "${TAG_SUFFIX}" && TAG="${TAG}-${TAG_SUFFIX}"

docker build -t "${TAG}" -f docker/Dockerfile.ollama . \
    && docker tag ${TAG} ${IMAGE_NAME}:latest
