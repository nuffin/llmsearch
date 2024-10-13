#!/usr/bin/env bash

set -x

IMAGE_NAME="semantic-search"

TAG="${IMAGE_NAME}:$(date +%m%d_%H%M)"

TAG_SUFFIX=$1
test ! -z "${TAG_SUFFIX}" && TAG="${TAG}-${TAG_SUFFIX}"

docker build -t "${TAG}" -f Dockerfile . \
    && docker tag ${TAG} ${IMAGE_NAME}:latest
