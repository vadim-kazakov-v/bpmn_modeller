from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

import os

# The API endpoint for the BPMN generator - configurable for Docker
BPMN_API_URL = os.environ.get('BPMN_API_URL', 'http://localhost:8000/generate-bpmn')
# In Docker, the backend service will be accessible as 'http://backend:8000/generate-bpmn'
# but we'll use the service name from environment variable
if os.environ.get('DOCKER_ENV') == 'true':
    BPMN_API_URL = "http://backend:8000/generate-bpmn"
else:
    BPMN_API_URL = os.environ.get('BPMN_API_URL', 'http://localhost:8000/generate-bpmn')

@app.route('/')
def index():
    # Default YAML example
    default_yaml = """# Example BPMN YAML definition
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
            type: "task"
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
        target: "EndEvent_1\""""
    
    return render_template('index.html', default_yaml=default_yaml)

@app.route('/generate-bpmn', methods=['POST'])
def generate_bpmn():
    try:
        yaml_content = request.json.get('yaml', '')
        
        # Make request to the backend API
        response = requests.post(BPMN_API_URL, json={'yaml': yaml_content})
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': response.json().get('detail', 'Error generating BPMN')}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/templates/index.html')
def template():
    # This route is just to make sure the template exists
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)