#!/usr/bin/env bash

ENVNAME=$1

env ENVIRONMENT=${ENVNAME} python3 src/app.py
