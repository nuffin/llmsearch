#!/usr/bin/env bash

set -x

FILEPATH=$(realpath $(dirname ${0}))
ROOTPATH=$(realpath ${FILEPATH}/..)

cd ${ROOTPATH}

IMAGE_NAME="llmpa-base"

TAG="${IMAGE_NAME}:$(date +%m%d_%H%M)"

TAG_SUFFIX=$1
test ! -z "${TAG_SUFFIX}" && TAG="${TAG}-${TAG_SUFFIX}"

docker build -t "${TAG}" -f docker/Dockerfile.base . \
    && docker tag ${TAG} ${IMAGE_NAME}:latest

# TAR_BALL_FILE_PATH="$(echo ${TAG} | sed "s,:,.,").tar.gz"
# docker build -t "${TAG}" -f Dockerfile.base . \
#     && docker tag ${TAG} ${IMAGE_NAME}:latest \
#     && docker save ${TAG} | gzip -9 > ${TAR_BALL_FILE_PATH} \
#     && echo Saved as ${TAR_BALL_FILE_PATH}
