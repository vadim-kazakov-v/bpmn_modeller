from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yaml
from lxml import etree
from typing import List, Dict, Any, Optional
import uuid

app = FastAPI(title="BPMN Generator API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YamlRequest(BaseModel):
    yaml: str

def create_bpmn_element(tag: str, attrib: Dict[str, str] = None, **kwargs) -> etree.Element:
    """Helper function to create BPMN elements"""
    if attrib is None:
        attrib = {}
    attrib.update(kwargs)
    return etree.Element(f"{{http://www.omg.org/spec/BPMN/20100524/MODEL}}{tag}", attrib)

def generate_bpmn_from_yaml(yaml_content: str) -> str:
    """Convert YAML workflow definition to BPMN 2.0 XML"""
    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")
    
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="YAML must represent a dictionary")
    
    # Create root BPMN element
    root = etree.Element(
        "{http://www.omg.org/spec/BPMN/20100524/MODEL}definitions",
        nsmap={
            None: "http://www.omg.org/spec/BPMN/20100524/MODEL",
            "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
            "dc": "http://www.omg.org/spec/DD/20100524/DC",
            "di": "http://www.omg.org/spec/DD/20100524/DI"
        },
        id=f"Definitions_{uuid.uuid4()}",
        targetNamespace="http://bpmn.io/schema/bpmn"
    )
    
    # Add process
    process_id = f"Process_{uuid.uuid4()}"
    process = create_bpmn_element("process", id=process_id, isExecutable="false")
    root.append(process)
    
    # Add collaboration for pools
    collaboration = create_bpmn_element("collaboration", id=f"Collaboration_{uuid.uuid4()}")
    
    # Process pools and lanes
    pools_data = data.get('pools', [])
    for pool_data in pools_data:
        pool_id = pool_data.get('id', f"Pool_{uuid.uuid4()}")
        pool_name = pool_data.get('name', 'Pool')
        
        # Add participant to collaboration
        participant = create_bpmn_element(
            "participant",
            id=pool_id,
            name=pool_name,
            processRef=process_id
        )
        collaboration.append(participant)
        
        # Process lanes
        lanes_data = pool_data.get('lanes', [])
        if lanes_data:
            lane_set = create_bpmn_element("laneSet", id=f"LaneSet_{uuid.uuid4()}")
            
            for lane_data in lanes_data:
                lane_id = lane_data.get('id', f"Lane_{uuid.uuid4()}")
                lane_name = lane_data.get('name', 'Lane')
                
                lane = create_bpmn_element("lane", id=lane_id, name=lane_name)
                
                # Add elements to lane
                elements = lane_data.get('elements', [])
                for element in elements:
                    element_ref = create_bpmn_element("flowNodeRef", text=element['id'])
                    lane.append(element_ref)
                
                lane_set.append(lane)
            
            process.insert(0, lane_set)  # Insert laneSet at the beginning of process
    
    # Add collaboration to root if there are pools
    if pools_data:
        root.insert(0, collaboration)
    
    # Process elements (tasks, events, gateways)
    for pool_data in pools_data:
        lanes_data = pool_data.get('lanes', [])
        for lane_data in lanes_data:
            elements = lane_data.get('elements', [])
            for element in elements:
                element_type = element['type']
                element_id = element['id']
                element_name = element.get('name', '')
                
                if element_type == 'startEvent':
                    elem = create_bpmn_element("startEvent", id=element_id, name=element_name)
                elif element_type == 'endEvent':
                    elem = create_bpmn_element("endEvent", id=element_id, name=element_name)
                elif element_type == 'task':
                    elem = create_bpmn_element("task", id=element_id, name=element_name)
                elif element_type == 'serviceTask':
                    elem = create_bpmn_element("serviceTask", id=element_id, name=element_name)
                elif element_type == 'userTask':
                    elem = create_bpmn_element("userTask", id=element_id, name=element_name)
                elif element_type == 'manualTask':
                    elem = create_bpmn_element("manualTask", id=element_id, name=element_name)
                elif element_type == 'exclusiveGateway':
                    elem = create_bpmn_element("exclusiveGateway", id=element_id, name=element_name)
                elif element_type == 'parallelGateway':
                    elem = create_bpmn_element("parallelGateway", id=element_id, name=element_name)
                elif element_type == 'inclusiveGateway':
                    elem = create_bpmn_element("inclusiveGateway", id=element_id, name=element_name)
                elif element_type == 'intermediateCatchEvent':
                    elem = create_bpmn_element("intermediateCatchEvent", id=element_id, name=element_name)
                elif element_type == 'intermediateThrowEvent':
                    elem = create_bpmn_element("intermediateThrowEvent", id=element_id, name=element_name)
                else:
                    # Default to task for unknown types
                    elem = create_bpmn_element("task", id=element_id, name=element_name)
                
                process.append(elem)
    
    # Process sequence flows
    for pool_data in pools_data:
        flows_data = pool_data.get('flows', [])
        for flow in flows_data:
            flow_id = flow.get('id', f"Flow_{uuid.uuid4()}")
            source_ref = flow['source']
            target_ref = flow['target']
            flow_name = flow.get('name', '')
            
            sequence_flow = create_bpmn_element(
                "sequenceFlow",
                id=flow_id,
                sourceRef=source_ref,
                targetRef=target_ref,
                name=flow_name
            )
            
            # Add condition expression if present
            condition = flow.get('condition')
            if condition:
                condition_elem = create_bpmn_element("conditionExpression", text=condition)
                sequence_flow.append(condition_elem)
            
            process.append(sequence_flow)
    
    # Add BPMNDI information for visualization
    bpmn_di = create_bpmn_element("BPMNDiagram", id=f"BPMNDiagram_{uuid.uuid4()}", name=data.get('name', 'Diagram'))
    plane = create_bpmn_element("BPMNPlane", id=f"BPMNPlane_{uuid.uuid4()}", bpmnElement=process_id)
    
    # Add basic shape and edge definitions for visualization
    for pool_data in pools_data:
        lanes_data = pool_data.get('lanes', [])
        for lane_data in lanes_data:
            elements = lane_data.get('elements', [])
            for element in elements:
                element_id = element['id']
                
                # Add BPMN shape for the element
                bounds = create_bpmn_element(
                    "Bounds", 
                    x="100", 
                    y="100", 
                    width="100", 
                    height="80"
                )
                shape = create_bpmn_element(
                    "BPMNShape", 
                    id=f"_BPMNShape_{element_id}", 
                    bpmnElement=element_id
                )
                shape.append(bounds)
                plane.append(shape)
    
    # Add flows to BPMNDI
    for pool_data in pools_data:
        flows_data = pool_data.get('flows', [])
        for flow in flows_data:
            flow_id = flow.get('id', f"Flow_{uuid.uuid4()}")
            
            edge = create_bpmn_element(
                "BPMNEdge", 
                id=f"_BPMNEdge_{flow_id}", 
                bpmnElement=flow_id
            )
            
            # Add waypoint elements for the edge
            waypoint1 = create_bpmn_element("waypoint", x="150", y="140")
            waypoint2 = create_bpmn_element("waypoint", x="250", y="140")
            edge.append(waypoint1)
            edge.append(waypoint2)
            
            plane.append(edge)
    
    bpmn_di.append(plane)
    root.append(bpmn_di)
    
    # Convert to string
    return etree.tostring(root, pretty_print=True, encoding='unicode')

@app.post("/generate-bpmn")
async def generate_bpmn(request: YamlRequest):
    """Generate BPMN XML from YAML definition"""
    try:
        bpmn_xml = generate_bpmn_from_yaml(request.yaml)
        return {"bpmn": bpmn_xml}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "BPMN Generator API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)