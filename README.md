# GLM Forge

A Python project for running inference in CI containers.

## Usage

1. Build the Docker image using the provided Dockerfile.
2. Run the image with a JSON payload file as an argument.

## Acceptance Criteria

* Docker image size < 200MB
* Exposes a /run-inference script that accepts a JSON payload file
* Script exits with 0 on success and non-zero on failure
