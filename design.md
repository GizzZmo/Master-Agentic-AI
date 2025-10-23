Here is a detailed, two-part documentation for the **Master-Agentic-AI Canvas Edition**, starting with the **Frontend Design** and then detailing the **Backend Execution**.

-----

## 5\. Frontend Design & Interactivity (React Flow / Cyberpunk Canvas) 💻

The Canvas Edition frontend is an interactive visualization tool that allows users to graphically design the multi-agent workflow. It's built primarily with **React** and the **React Flow** library, maintaining the original project’s **cyberpunk aesthetic**.

### A. Interface Components

The user interface is divided into three main areas:

1.  **Node Palette (Left Sidebar):** A fixed panel listing all available agents and logic blocks. Nodes are dragged from here onto the canvas.
      * *Aesthetic:* Dark slate background with agent names rendered in neon green monospace font.
2.  **Interactive Canvas (Center):** The main workspace where nodes are placed, connected, and rearranged.
      * *Aesthetic:* Deep purple-black background. Active execution will feature glowing node borders and pulsating connections.
3.  **Settings & Trace Panel (Right Sidebar):** A dynamic panel that changes its content based on what is selected on the canvas.
      * *Default View:* **Execution Trace Log** (real-time stream of agent activity).
      * *Node Selected View:* **Configuration Form** for the selected agent/node.

### B. Custom Node Design and Styling

All four core agents are rendered as custom **React Flow nodes** with distinct visual characteristics to aid in quick identification.

| Node Type | Shape/Icon | Primary Neon Color | Key Data Ports |
| :--- | :--- | :--- | :--- |
| **Master Agent** | Octagon (Start/End) | **Electric Blue** | 1 Output (Goal), 1 Input (Final Result) |
| **Planning Agent** | Diamond (Strategy) | **Neon Yellow** | 1 Input (Goal), 1 Output (Plan JSON) |
| **Execution Agent** | Square (Action) | **Lime Green** | 1 Input (Step), 1 Output (Observation/Result) |
| **Ethics Agent** | Shield/Badge | **Vibrant Red/Magenta** | 1 Input (Content), 2 Outputs (Approved, Flagged) |

### C. Interactivity and Observability

The Canvas is designed to be a **live debugging and observability tool** for the running MAS.

  * **Drag-and-Drop Workflow:** Users create the workflow by dragging nodes from the palette and connecting their ports using click-and-drag edges. Connections define the data flow and execution order (e.g., the output of the **Planner** connects to the input of the **Ethics Agent**).
  * **Live Trace:** When a task is initiated:
      * The entire workflow shifts to a dark, semi-transparent state.
      * The currently executing node (e.g., the **Planning Agent**) lights up with its corresponding neon color.
      * The edge carrying data (e.g., the "Plan" edge) flashes or pulsates, showing the flow.
      * Detailed, line-by-line **ReAct** or **CoT** monologues from the active agent are streamed into the **Trace Panel**.
  * **Error Visualization:** If a tool call fails or the Ethics Agent flags a critical violation, the responsible node’s border flashes a distinct **Warning Yellow** or turns **Critical Red**, and the execution flow halts at that node.

### D. Data Serialization and API Payload

When the user clicks "Run," the frontend must translate the visual graph into a structured format for the backend.

1.  **Gather State:** React Flow's state (`nodes`, `edges`) is retrieved.
2.  **Generate JSON Graph:** This state is serialized into a single **JSON object** that the Python backend's graph framework (LangGraph) can parse.

**Example JSON Payload Snippet:**

```json
{
  "prompt": "Find the best recipe for kimchi and review its safety.",
  "workflow_name": "Kimchi Recipe Finder",
  "graph_structure": {
    "nodes": [
      {"id": "n1", "type": "masterAgent", "config": {"persona": "Culinary AI"}},
      {"id": "n2", "type": "planningAgent", "config": {"cot_level": "Detailed"}},
      {"id": "n3", "type": "ethicsAgent", "config": {"review_mode": "Plan"}},
      // ... other nodes
    ],
    "edges": [
      {"source": "n1", "sourceHandle": "output", "target": "n2", "targetHandle": "input"},
      {"source": "n2", "sourceHandle": "plan_output", "target": "n3", "targetHandle": "plan_input"}
      // ... other connections
    ]
  }
}
```

-----

## 6\. Backend Execution & Logic (FastAPI / LangGraph) ⚙️

The backend remains a high-performance **FastAPI** application, but the core **MasterAgentOrchestrator** logic is replaced by a dynamic **LangGraph** engine that executes the user-defined workflow.

### A. The `/execute-graph` Endpoint

A new, dedicated asynchronous API endpoint is created to handle canvas execution:

  * **Endpoint:** `POST /api/v1/execute-graph`
  * **Input:** The JSON Graph Structure payload sent from the frontend.
  * **Output:** A **Server-Sent Event (SSE)** stream used to send real-time execution updates back to the frontend for the live trace and node status visualization.

### B. Dynamic Graph Instantiation (LangGraph)

The key challenge is converting the static JSON into a runnable Python graph structure.

1.  **Parse JSON:** FastAPI receives the JSON payload.
2.  **Define Agent Functions:** Each of the four core agents (Planner, Executor, Ethics) is implemented as a reusable **Python function** (`def planner_node(...)`, `def ethics_node(...)`) that takes the graph state and returns an output.
3.  **Build Graph State:** A shared `State` object is defined (using `TypedDict` or `Pydantic`) to store all context that flows between the nodes (e.g., `user_prompt`, `current_plan`, `current_step_result`, `ethics_flag`).
4.  **Instantiate Graph:** LangGraph is used to dynamically build the `StatefulGraph` based on the user's connections:
      * **Nodes:** The Python functions are mapped to the `nodes` defined in the JSON.
      * **Edges:** The connections (`edges` in the JSON) are used to define the **data flow** between the Python functions.
      * **Conditional Edges:** The **Ethics Agent** node maps directly to a LangGraph **conditional edge**. The `ethics_node` function returns a signal (`"FLAGGED"` or `"APPROVED"`), and the LangGraph router directs execution to the appropriate subsequent node (e.g., if `"FLAGGED"`, route back to the Planner for revision).

### C. Execution Flow and Real-Time Streaming

The backend's main loop focuses on executing the LangGraph and pushing results to the SSE stream.

1.  **Initialization:** The graph run starts by injecting the `user_prompt` into the initial `State`.
2.  **Graph Run:** The `graph.stream()` method in LangGraph is utilized. This method allows the process to yield results at every node transition.
3.  **SSE Generator:** A generator function is used in FastAPI to capture these streamed outputs and format them as SSE events.

**Example SSE Event Structure (Sent to Frontend):**

| Event | Data Field | Description |
| :--- | :--- | :--- |
| `node_start` | `node_id`, `timestamp` | Signal the frontend to highlight this node. |
| `agent_thought` | `node_id`, `monologue` | Stream the agent's real-time CoT/ReAct internal reasoning. |
| `tool_call` | `tool_name`, `args` | Indicate the start of a simulated external tool call. |
| `node_output` | `node_id`, `state_update` | The result of the node's function; update the frontend's trace log. |
| `graph_end` | `final_result` | The synthesized final answer; execution completed. |

This dynamic, graph-based execution system ensures that the backend precisely follows the complex, custom logic designed by the user on the Canvas, delivering both the final result and the critical **observability** required for advanced agentic development.
