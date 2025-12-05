# Docker Setup for BPMN 2.0 Generator with Flask UI

This document describes how to run the BPMN 2.0 Generator with Flask UI using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Running the Application

### Quick Start

To build and run the entire application stack:

```bash
./run_docker.sh
```

Or manually:

```bash
docker-compose up --build
```

### Accessing the Services

Once the containers are running, you can access the services at:

- **Flask UI**: http://localhost:5000
- **Backend API**: http://localhost:8000 (internal - accessed through Flask UI)

## Docker Architecture

The application consists of two main services:

### 1. Flask UI Service (`flask_ui`)
- Serves the web interface
- Runs on port 5000
- Built from `Dockerfile.flask_ui`
- Communicates with the backend service

### 2. Backend Service (`backend`)
- Handles BPMN generation logic
- Runs on port 8000 internally
- Built from `Dockerfile.backend`
- Accessible via the `backend` service name from other containers

## Docker Files

- `Dockerfile.flask_ui`: Defines the Flask UI container
- `Dockerfile.backend`: Defines the backend API container
- `docker-compose.yml`: Orchestrates both services
- `run_docker.sh`: Convenience script to start the application

## Development with Docker

For development, the compose file mounts your local files into the containers so you can edit code locally and see changes reflected immediately (for the Flask app, you may need to restart the container for some changes to take effect).

## Troubleshooting

### Common Issues

1. **Port already in use**: Make sure ports 5000 and 8000 are available on your system.

2. **Dependency issues**: If you encounter dependency issues, try rebuilding the images:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

3. **API communication failure**: The Flask UI container should automatically connect to the backend service using the internal DNS name `backend`. If you're having connection issues, make sure both services are running.

### Viewing Logs

To view logs from individual services:

```bash
# View all logs
docker-compose logs

# View Flask UI logs
docker-compose logs flask_ui

# View backend logs
docker-compose logs backend
```

## Stopping the Application

To stop the running services:

```bash
# In another terminal
docker-compose down
```

Or press `Ctrl+C` in the terminal where you started the services.