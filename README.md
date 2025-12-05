# BPMN 2.0 Generator from YAML

This application allows you to define BPMN 2.0 workflows using a YAML format and visualize them in a browser-based editor.

## Features

- YAML-based BPMN 2.0 workflow definition
- Real-time BPMN diagram visualization
- Support for pools, lanes, tasks, events, and gateways
- Download BPMN XML files
- Dark mode UI

## Architecture

The application consists of:
- **Frontend**: React application with Monaco editor for YAML editing and bpmn-js for diagram visualization
- **Backend**: FastAPI server that converts YAML to BPMN 2.0 XML
- **Docker**: Containerized deployment with docker-compose

## Prerequisites

- Docker
- Docker Compose

## Running the Application

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## YAML Format

See [BPMN_YAML_FORMAT.md](./BPMN_YAML_FORMAT.md) for detailed documentation on the YAML format.

## Development

To run the application in development mode:

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Technologies Used

- **Frontend**: React, Monaco Editor, bpmn-js
- **Backend**: Python, FastAPI, PyYAML, lxml
- **Containerization**: Docker, Docker Compose
- **BPMN Standard**: BPMN 2.0 compliant

## Example Workflow

```yaml
name: "Order Processing Workflow"
pools:
  - id: "Pool1"
    name: "Order Management"
    lanes:
      - id: "Lane1"
        name: "Order Reception"
        elements:
          - id: "StartEvent_1"
            type: "startEvent"
            name: "Order Received"
          - id: "Task_1"
            type: "task"
            name: "Validate Order"
          - id: "Gateway_1"
            type: "exclusiveGateway"
            name: "Valid Order?"
          - id: "Task_2"
            type: "serviceTask"
            name: "Process Payment"
          - id: "EndEvent_1"
            type: "endEvent"
            name: "Order Processed"
    flows:
      - id: "Flow_1"
        source: "StartEvent_1"
        target: "Task_1"
      - id: "Flow_2"
        source: "Task_1"
        target: "Gateway_1"
      - id: "Flow_3"
        source: "Gateway_1"
        target: "Task_2"
      - id: "Flow_4"
        source: "Task_2"
        target: "EndEvent_1"
```