#!/usr/bin/env bash

docker build -t postgres-pgvector:latest -f docker/Dockerfile.postgres+pgvector .
