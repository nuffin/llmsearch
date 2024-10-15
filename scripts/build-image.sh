#!/usr/bin/env bash

set -x

FILEPATH=$(realpath $(dirname ${0}))
ROOTPATH=$(realpath ${FILEPATH}/..)

cd ${ROOTPATH}

IMAGE_NAME="llmsearch"

TAG="${IMAGE_NAME}:$(date +%m%d_%H%M)"

TAG_SUFFIX=$1
test ! -z "${TAG_SUFFIX}" && TAG="${TAG}-${TAG_SUFFIX}"

docker build -t "${TAG}" -f docker/Dockerfile . \
    && docker tag ${TAG} ${IMAGE_NAME}:latest
