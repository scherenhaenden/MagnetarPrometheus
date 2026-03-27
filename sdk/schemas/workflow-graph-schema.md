# MagnetarPrometheus UI Graph Model Schema

## 1. Objective

This document defines the schema for the UI Graph Model. The purpose of this schema is to provide a language-neutral, serialized representation of a workflow suitable for visual drag-and-drop editing.

This UI Graph Model maps directly back to the underlying runtime schema (defined in `sdk/python/src/magnetar_prometheus_sdk/models.py`), ensuring that workflows created in the UI can be seamlessly executed by the orchestration engine.

## 2. Core Concepts

The visual graph consists of three primary entities:

*   **Workflow Metadata:** Represents the overall workflow and its global settings.
*   **Nodes:** Represent individual `StepDefinition` instances in the workflow.
*   **Edges:** Represent execution transitions (`next` conditions) between steps.

## 3. Schema Definitions

The schema is defined conceptually using JSON/YAML structures.

### 3.1 Workflow Graph Representation

The root object representing the visual graph.

```yaml
type: object
properties:
  id:
    type: string
    description: "Unique identifier for the workflow (maps to Workflow.id)"
  name:
    type: string
    description: "Human-readable name for the workflow (maps to Workflow.name)"
  version:
    type: string
    description: "Version string (maps to Workflow.version)"
  start_node_id:
    type: string
    description: "ID of the node where execution begins (maps to Workflow.start_step)"
  settings:
    type: object
    description: "Global workflow settings (maps to Workflow.settings)"
  nodes:
    type: array
    items:
      $ref: "#/definitions/Node"
    description: "List of all nodes (steps) in the graph"
  edges:
    type: array
    items:
      $ref: "#/definitions/Edge"
    description: "List of all execution paths (transitions) between nodes"
```

### 3.2 Node Schema (Maps to `StepDefinition`)

A node represents an executable step. It contains UI-specific metadata (like visual position) and the core step configuration.

```yaml
definitions:
  Node:
    type: object
    properties:
      id:
        type: string
        description: "Unique ID for this node (maps to the step key in Workflow.steps)"
      type:
        type: string
        description: "The type of step (e.g., 'email.fetch', 'ai.classify') (maps to StepDefinition.type)"
      executor:
        type: string
        description: "The executor to run this step (e.g., 'python') (maps to StepDefinition.executor)"
      config:
        type: object
        description: "Step-specific configuration parameters (maps to StepDefinition.config)"
      ui_metadata:
        type: object
        description: "UI-only properties for visual rendering"
        properties:
          position:
            type: object
            properties:
              x: { type: number }
              y: { type: number }
          label:
            type: string
            description: "Custom display label for the node in the UI"
          description:
            type: string
            description: "Optional notes or documentation for the node"
```

### 3.3 Edge Schema (Maps to `StepDefinition.next`)

An edge represents a path from one node to another. It encapsulates the routing logic defined in the `next` attribute of a `StepDefinition`.

```yaml
definitions:
  Edge:
    type: object
    properties:
      id:
        type: string
        description: "Unique identifier for the edge (used purely by the UI graph)"
      source_node_id:
        type: string
        description: "ID of the originating node"
      target_node_id:
        type: string
        description: "ID of the destination node"
      condition:
        type: object
        description: "Optional condition that must evaluate to true for this edge to be traversed"
        properties:
          type:
            type: string
            enum: ["default", "conditional", "error_path"]
            description: "Type of transition. 'default' is unconditional. 'conditional' implies a rule evaluation. 'error_path' handles failures."
          expression:
            type: string
            description: "The actual condition string (e.g., \"context['ai']['decision'] == 'create_ticket'\")"
```

## 4. Mapping to Runtime Models

The UI Graph Model is an intermediate representation. The UI application must translate between this Graph Model and the Backend Runtime Models.

### 4.1 UI Graph to Backend `Workflow`

When saving or executing from the UI:

1.  **Workflow Mapping:**
    *   Graph `id`, `name`, `version`, `settings` map 1:1 to `Workflow` attributes.
    *   Graph `start_node_id` maps to `Workflow.start_step`.
2.  **Step Mapping:**
    *   Iterate through Graph `nodes`. Each node becomes an entry in the `Workflow.steps` dictionary.
    *   The dictionary key is the `Node.id`.
    *   `StepDefinition.type`, `executor`, and `config` are copied directly from the Node.
3.  **Next/Routing Mapping:**
    *   For a given `Node.id`, find all outgoing `Edges` (where `source_node_id == Node.id`).
    *   If there is exactly one unconditional edge (`condition.type == 'default'`), `StepDefinition.next` is set to the `target_node_id` string.
    *   If there are multiple conditional edges, `StepDefinition.next` becomes a complex object (e.g., `mode: conditional`, with a list of conditions mapping to `target_node_id`).

### 4.2 Backend `Workflow` to UI Graph

When loading an existing workflow into the UI:

1.  **Workflow Mapping:**
    *   Create the base graph object with `Workflow` properties.
2.  **Node Generation:**
    *   For each key-value pair in `Workflow.steps`, create a `Node`.
    *   Assign default UI metadata (e.g., auto-layout x/y coordinates) if none exists.
3.  **Edge Generation:**
    *   Analyze the `next` attribute of each `StepDefinition`.
    *   If `next` is a simple string, create a default `Edge` to the target node.
    *   If `next` is a conditional block, create multiple `Edge`s, storing the expression in the `Edge.condition` object.
