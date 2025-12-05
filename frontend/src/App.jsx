import React, { useState, useRef } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import './App.css';

function App() {
  const [yamlInput, setYamlInput] = useState(`# Example BPMN YAML definition
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
        target: "EndEvent_1"
`);
  const [bpmnXml, setBpmnXml] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const iframeRef = useRef(null);

  const handleGenerateBpmn = async () => {
    setIsLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/generate-bpmn', {
        yaml: yamlInput
      });
      setBpmnXml(response.data.bpmn);
      
      // Update iframe with the BPMN diagram
      if (iframeRef.current) {
        const iframeDoc = iframeRef.current.contentDocument;
        if (iframeDoc) {
          iframeDoc.open();
          iframeDoc.write(`
            <!DOCTYPE html>
            <html>
            <head>
              <title>BPMN Diagram</title>
              <script src="https://unpkg.com/bpmn-js@16.0.0/dist/bpmn-viewer.development.js"></script>
              <style>
                body { margin: 0; }
                #canvas { width: 100%; height: 100vh; }
              </style>
            </head>
            <body>
              <div id="canvas"></div>
              <script>
                const viewer = new BpmnJS({ container: '#canvas' });
                viewer.importXML(\`${response.data.bpmn}\`).then(function(result) {
                  const { warnings } = result;
                  if (warnings && warnings.length) {
                    console.log('BPMN import warnings:', warnings);
                  }
                  // Fit the diagram to the viewport after import
                  viewer.get('canvas').zoom('fit-viewport');
                  viewer.get('canvas').scroll({ x: 0, y: 0 });
                }).catch(function(err) {
                  console.error('BPMN import error:', err);
                  // Display error message in the canvas
                  document.getElementById('canvas').innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: red; font-size: 18px;">Error displaying BPMN diagram: ' + err.message + '</div>';
                });
              </script>
            </body>
            </html>
          `);
          iframeDoc.close();
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!bpmnXml) return;
    
    const blob = new Blob([bpmnXml], { type: 'application/xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'diagram.bpmn';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>BPMN 2.0 Generator from YAML</h1>
        <p>Define your workflow in YAML and generate BPMN 2.0 diagrams</p>
      </header>
      
      <div className="main-container">
        <div className="editor-section">
          <div className="section-header">
            <h2>YAML Input</h2>
            <button 
              onClick={handleGenerateBpmn} 
              disabled={isLoading}
              className="generate-btn"
            >
              {isLoading ? 'Generating...' : 'Generate BPMN'}
            </button>
          </div>
          <div className="editor-container">
            <Editor
              height="500px"
              defaultLanguage="yaml"
              defaultValue={yamlInput}
              onChange={(value) => setYamlInput(value)}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                scrollBeyondLastLine: false,
                automaticLayout: true,
              }}
            />
          </div>
          
          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}
        </div>
        
        <div className="preview-section">
          <div className="section-header">
            <h2>BPMN Diagram Preview</h2>
            {bpmnXml && (
              <button onClick={handleDownload} className="download-btn">
                Download BPMN
              </button>
            )}
          </div>
          <div className="preview-container">
            <iframe 
              ref={iframeRef} 
              title="BPMN Preview" 
              style={{ width: '100%', height: '100%', border: 'none' }}
            />
          </div>
        </div>
      </div>
      
      <div className="documentation-section">
        <h2>YAML Format Documentation</h2>
        <div className="doc-content">
          <h3>Structure:</h3>
          <pre>
{`name: "Workflow Name"
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
            # Additional properties based on element type
    flows:
      - id: "Flow ID"
        source: "Source Element ID"
        target: "Target Element ID"`
}
          </pre>
          
          <h3>Element Types:</h3>
          <ul>
            <li><strong>startEvent</strong>: Process start point</li>
            <li><strong>endEvent</strong>: Process end point</li>
            <li><strong>task</strong>: Manual task</li>
            <li><strong>serviceTask</strong>: Automated task</li>
            <li><strong>exclusiveGateway</strong>: Decision point</li>
            <li><strong>parallelGateway</strong>: Split/join point</li>
            <li><strong>inclusiveGateway</strong>: Conditional gateway</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;