# BPMN 2.0 YAML Format Specification

This document describes the YAML format for defining BPMN 2.0 workflows and the conversion logic.

## Overall Structure

```yaml
name: "Workflow Name"                    # Name of the BPMN diagram
pools:                                  # List of pools (participants)
  - id: "Pool1"                         # Unique identifier for the pool
    name: "Order Management"            # Display name for the pool
    lanes:                              # List of lanes within the pool
      - id: "Lane1"                     # Unique identifier for the lane
        name: "Order Reception"         # Display name for the lane
        elements:                       # List of BPMN elements in this lane
          - id: "StartEvent_1"          # Unique identifier for the element
            type: "startEvent"          # Type of BPMN element
            name: "Order Received"      # Display name for the element
            # Additional properties based on element type
        flows:                          # List of sequence flows in this pool
          - id: "Flow_1"                # Unique identifier for the flow
            source: "StartEvent_1"      # Source element ID
            target: "Task_1"            # Target element ID
            name: "From start to task"  # Optional display name for the flow
            condition: "isValidOrder"   # Optional condition expression
```

## Element Types

### Events
- `startEvent`: Process start point
- `endEvent`: Process end point
- `intermediateCatchEvent`: Intermediate event that catches something
- `intermediateThrowEvent`: Intermediate event that throws something

### Tasks
- `task`: Generic task (manual)
- `serviceTask`: Automated task
- `userTask`: Task performed by a user
- `manualTask`: Manual task with no business logic

### Gateways
- `exclusiveGateway`: Decision point with one path chosen
- `parallelGateway`: Split/join point with multiple paths
- `inclusiveGateway`: Conditional gateway allowing multiple paths

## Detailed Format Rules

### Root Level
- `name` (string): The overall name of the BPMN diagram
- `pools` (list): List of pools that participate in the process

### Pool Level
- `id` (string): Unique identifier for the pool
- `name` (string): Display name for the pool
- `lanes` (list): List of lanes within the pool
- `flows` (list): List of sequence flows that connect elements in the pool

### Lane Level
- `id` (string): Unique identifier for the lane
- `name` (string): Display name for the lane
- `elements` (list): List of BPMN elements in this lane

### Element Level
- `id` (string): Unique identifier for the element (must be unique across the entire diagram)
- `type` (string): Type of BPMN element (see element types above)
- `name` (string): Display name for the element

### Flow Level
- `id` (string): Unique identifier for the sequence flow
- `source` (string): ID of the source element
- `target` (string): ID of the target element
- `name` (string, optional): Display name for the flow
- `condition` (string, optional): Condition expression for conditional flows

## Example Complete YAML Definition

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
        name: "Receive Order"
      - id: "Flow_2"
        source: "Task_1"
        target: "Gateway_1"
        name: "Validation Complete"
      - id: "Flow_3"
        source: "Gateway_1"
        target: "Task_2"
        name: "Order Valid"
        condition: "isValidOrder"
      - id: "Flow_4"
        source: "Task_2"
        target: "EndEvent_1"
        name: "Payment Processed"
```

## Conversion Logic

The conversion from YAML to BPMN 2.0 XML follows these steps:

1. Parse the YAML into a data structure
2. Create the root BPMN definitions element with proper namespaces
3. Create a collaboration element if there are multiple pools
4. Create participants for each pool
5. Create lane sets for each pool that has lanes
6. Create process elements for each pool
7. Add BPMN elements (tasks, events, gateways) to the process
8. Add sequence flows between elements
9. Generate BPMNDI information for visualization
10. Serialize to XML format

The resulting BPMN 2.0 XML is compliant with the OMG BPMN 2.0 specification and can be visualized in any BPMN-compliant tool.