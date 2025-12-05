#!/bin/bash

# Script to start both the backend API and Flask UI

echo "Starting BPMN Generator backend API..."
cd /workspace/backend
python main.py > server.log 2>&1 &
BACKEND_PID=$!
echo "Backend API started with PID: $BACKEND_PID"

sleep 3  # Wait for backend to start

echo "Starting Flask UI..."
cd /workspace
python flask_ui.py > flask_ui.log 2>&1 &
FLASK_PID=$!
echo "Flask UI started with PID: $FLASK_PID"

echo ""
echo "Servers are running:"
echo "Backend API: http://localhost:8000"
echo "Flask UI: http://localhost:5000"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Flask UI PID: $FLASK_PID"
echo ""
echo "To stop the servers, run: pkill -f 'python.*main.py\|python.*flask_ui.py'"