#!/usr/bin/env bash
# Compose spec:
# services:
#   open-meteo:
#     image: ghcr.io/open-meteo/open-meteo
#     container_name: open-meteo
#     volumes:
#       - open-meteo-data:/app/data
#     ports:
#       - 9090:8080
#     restart: unless-stopped
#     
## Get the latest image
docker pull ghcr.io/open-meteo/open-meteo

# Create a Docker volume to store weather data
docker volume create --name open-meteo-data

# Start the API service on http://127.0.0.1:8080
docker run -d --rm -v open-meteo-data:/app/data -p 8080:8080 ghcr.io/open-meteo/open-meteo

# Download the latest ECMWF IFS 0.4° open-data forecast for temperature (50 MB)
docker run -it --rm -v open-meteo-data:/app/data ghcr.io/open-meteo/open-meteo sync ecmwf_ifs04 temperature_2m

# Get your forecast
curl "http://127.0.0.1:8080/v1/forecast?latitude=47.1&longitude=8.4&models=ecmwf_ifs04&hourly=temperature_2m"
