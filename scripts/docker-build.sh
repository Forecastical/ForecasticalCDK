#!/usr/bin/env bash

# Get the script dir
SCRIPT_DIR=$(dirname $0)
# Get dir of the project
PROJECT_DIR=$(dirname $SCRIPT_DIR)

# Ensure local registry is running
#docker pull registry:latest
#docker run registry || docker run -d -p 5000:5000 --restart=always --name registry registry:latest


# Build Backend
docker build $PROJECT_DIR/backend -t docker.io/trmolinaw/forecastical:backend
# Build Frontend

