# Flask UI for BPMN 2.0 Generator

This Flask-based UI provides a web interface for the BPMN 2.0 Generator that converts YAML workflow definitions into BPMN diagrams.

## Features

- YAML editor with syntax highlighting
- Real-time BPMN diagram preview
- Download functionality for generated BPMN files
- Comprehensive documentation of YAML format
- Error handling and validation

## Requirements

- Python 3.7+
- Flask
- requests
- The backend FastAPI server running on port 8000

## Installation

1. Install the required packages:
```bash
pip install -r flask_ui_requirements.txt
```

2. Make sure the backend FastAPI server is running:
```bash
cd backend
python main.py
```

3. Run the Flask UI:
```bash
python flask_ui.py
```

## Usage

1. Access the UI at `http://localhost:5000`
2. Enter or modify the YAML workflow definition in the left panel
3. Click "Generate BPMN" to create and visualize the diagram
4. Use the "Download BPMN" button to save the generated XML file

## YAML Format

The YAML format supports:

- **Pools**: Organizational boundaries
- **Lanes**: Subdivisions within pools
- **Elements**: Various BPMN elements like tasks, events, gateways
- **Flows**: Connections between elements

Example structure:
```yaml
name: "Workflow Name"
pools:
  - id: "Pool ID"
    name: "Pool Name"
    lanes:
      - id: "Lane ID"
        name: "Lane Name"
        elements:
          - id: "Element ID"
            type: "elementType"
            name: "Element Name"
    flows:
      - id: "Flow ID"
        source: "Source Element ID"
        target: "Target Element ID"
```

## Supported Element Types

- `startEvent`: Process start point
- `endEvent`: Process end point
- `task`: Manual task
- `serviceTask`: Automated task
- `userTask`: User task
- `manualTask`: Manual task
- `exclusiveGateway`: Decision point
- `parallelGateway`: Split/join point
- `inclusiveGateway`: Conditional gateway
- `intermediateCatchEvent`: Intermediate event
- `intermediateThrowEvent`: Intermediate event