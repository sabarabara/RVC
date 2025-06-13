#!/usr/bin/env bash
#
# Runs RVC API in Docker.

set -e

tag="rvc"

# Build image with tag
docker build -t "${tag}" .

# Run container with necessary ports and volumes
docker run -it --rm \
  -p 8000:8000 \
  -p 8001:8001 \
  -v "${PWD}/assets/weights:/weights:ro" \
  -v "${PWD}/assets/indices:/indices:ro" \
  -v "${PWD}/assets/audios:/audios:ro" \
  "${tag}"

