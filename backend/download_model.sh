#!/usr/bin/env bash

#Github Forecastical/Forecastical release 'Vision Model'
VISION_MODEL_URL='github.com/Forecastical/Forecastical/releases/download/v1.0/vision_model.pth'

# Check if the file exists
# ./model/vision_model.pth
if [ -f ./model/vision_model.pth ]; then
    echo "File exists"
else
    echo "File does not exist"
    # Download the file
    wget $VISION_MODEL_URL -P ./model
fi
