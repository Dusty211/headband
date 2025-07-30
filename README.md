# Headband

## Setup and Installation

This project is managed with Docker and Docker Compose. Ensure you have Docker installed on your system before proceeding.

### 1. Environment Configuration

An environment file is required to run the application. A sample file is provided at the root of the project.

Copy the sample environment file to create your local configuration:

```bash
cp .env.sample ./envs/backend.env
```

After copying, review and update the variables in `./envs/backend.env` as needed for your local setup.

### 2. Build and Run the Application

With Docker running, use the development compose file to build the images and start the services:

```bash
docker compose -f compose-dev.yaml up --build
```

This command will start all the necessary services, including the API, MCP, and NGINX. The API will be accessible at `http://localhost:8000`.

## Development with Devcontainers

This project is configured to be used with [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).

When you open this project in a devcontainer, VS Code automatically attaches to the running `api` service defined in `compose-dev.yaml`. Port forwarding is also handled automatically.

You can access the API from your local machine at `http://localhost:8000` just as you would if you were running the application locally. No extra configuration is needed.
