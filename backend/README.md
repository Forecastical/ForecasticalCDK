# Dev Guide
## Running the Backend.
The preferred way to run is via Docker:
1. After a code change, rebuild the container: `docker build . -t backend`
2. Run the container: `docker run --publish 8080:8080 backend`
3. Access the APIs via: `curl 0.0.0.0:8080`

## Making & Testing changes.
After a code change or a Dockerfile change, **PLEASE** ensure that the docker container builds and runs as intended BEFORE pushing the code.
- `docker build . -t backend && docker run --publish 8080:8080 backend`

