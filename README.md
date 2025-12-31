# Master-Agentic-AI
(MAS)

The "Master Agentic AI" application is a sophisticated Multi-Agent System (MAS) designed to embody the principles outlined in the provided blueprint, "Architecting the Agentic-Inclusive AI." It features a cyberpunk-themed user interface and allows users to integrate their own Gemini API key.

## Master Agentic AI: System Overview

This application is built as a full-stack solution, comprising a React frontend and a FastAPI backend. It implements a modular, multi-agent architecture to overcome the limitations of monolithic LLM prompting, as detailed in the blueprint.

### Architecture and Design Choices

The core of this application's design is a direct translation of the "Agentic-Inclusive AI" blueprint into a functional MAS.

1.  **Multi-Agent System (MAS) Architecture**:
    *   **Orchestrator Agent (MasterAgentOrchestrator)**: This is the "Super Agent" from the blueprint. It acts as the central coordinator, receiving user requests, decomposing them, delegating tasks to specialized sub-agents, and synthesizing their outputs. This addresses the blueprint's recommendation to move beyond a single, monolithic prompt.
    *   **Planning Agent (PlanningAgent)**: Responsible for breaking down complex goals into logical, step-by-step plans using Chain-of-Thought (CoT) reasoning. This agent's prompt is focused solely on planning, reducing the "curse of instructions" problem.
    *   **Execution Agent (ExecutionAgent)**: Implements the ReAct (Reason + Act) framework. It takes a step from the plan, decides which external tool to use, executes it, and processes the observation. This grounds the AI's reasoning in real-world interactions, mitigating hallucination.
    *   **Ethics & Safety Review Agent (EthicsAgent)**: This agent embodies the "Ethical and Inclusive Foundation" of the blueprint. It reviews plans and outputs against a "Constitution" (simulating Constitutional AI principles) to ensure fairness, safety, and ethical compliance. It can critique and suggest revisions, simulating the self-correction aspect of CAI.

2.  **Agentic Nature Implementation**:
    *   **Autonomy & Proactivity**: The `MasterAgentOrchestrator` is designed to take initiative in guiding the process, breaking down tasks, and managing the flow without constant human intervention after the initial prompt.
    *   **Planning & Reasoning (CoT)**: The `PlanningAgent` explicitly uses CoT by being prompted to "think step by step" and output a detailed plan.
    *   **Resourcefulness & Tool Use (ReAct)**: The `ExecutionAgent` is equipped with a `ToolRegistry` and follows the Thought-Action-Observation loop, allowing it to "simulate the use of tools" as described in the blueprint.
    *   **Learning & Adaptation (Simulated)**: While true continuous learning requires more complex infrastructure, the `EthicsAgent`'s ability to critique and suggest revisions, which can then be fed back into the planning/execution loop by the `Orchestrator`, simulates an adaptive feedback loop.

3.  **Ethical & Inclusive Foundation Implementation**:
    *   **Constitutional AI (CAI) Simulation**: A `constitution.py` file holds the core ethical principles derived directly from the blueprint. The `EthicsAgent` is explicitly instructed to "consult its Constitution" via a `retrieve_constitution` tool (a simulated RAG call). This makes the AI's values explicit and auditable, aligning with CAI principles.
    *   **Bias Mitigation**: The `EthicsAgent`'s role includes identifying and mitigating biases by reviewing plans and outputs against the constitutional principles. If a request is harmful, it politely declines and offers ethical alternatives, a hallmark of CAI-trained models.

4.  **Technical Realities & Mitigations**:
    *   **Context Window Management (RAG Simulation)**: The detailed "Constitution" is stored separately (`constitution.py`) and "retrieved" by the `EthicsAgent` only when needed. This prevents the core ethical principles from being pushed out of the LLM's context window during long conversations, addressing the "context window bottleneck" and "lost in the middle" problems.
    *   **Modular & Hierarchical Prompts**: Each agent has a focused, shorter prompt tailored to its specific role. This significantly reduces the "curse of instructions" by delegating different sets of instructions to different specialized agents.
    *   **Error Handling & Self-Correction**: The `MasterAgentOrchestrator` is designed to receive feedback (e.g., from the `EthicsAgent` or simulated tool failures) and can re-initiate planning or execution steps based on this feedback, simulating resilience.

### Technology Stack

*   **Frontend**:
    *   **React (with Vite)**: A modern JavaScript library for building user interfaces, chosen for its component-based architecture and efficient development. Vite provides a fast development experience.
    *   **Tailwind CSS**: A utility-first CSS framework for rapidly building custom designs. It's used to implement the cyberpunk theme with dark backgrounds, neon accents, and monospace fonts.
    *   **Axios**: A promise-based HTTP client for making requests to the backend.
*   **Backend**:
    *   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+. It's chosen for its asynchronous capabilities, Pydantic for data validation, and automatic OpenAPI documentation.
    *   **Google Generative AI (`google-generativeai`)**: The official Python SDK for interacting with the Gemini API.
    *   **Pydantic**: Used for data validation and settings management, ensuring robust API endpoints.
    *   **python-dotenv**: For loading environment variables (like the Gemini API key).
*   **Containerization**:
    *   **Docker**: For packaging the application into portable containers, ensuring consistent environments across development and deployment.
    *   **Docker Compose**: For defining and running multi-container Docker applications, simplifying the setup of both frontend and backend services.

### Cyberpunk Theme

The application's aesthetic is inspired by cyberpunk:
*   **Color Palette**: Dominated by dark blues, purples, and blacks, accented with vibrant neon greens, blues, and magentas.
*   **Typography**: Monospace fonts (e.g., 'Fira Code', 'Roboto Mono') are used to evoke a terminal-like feel.
*   **UI Elements**: Subtle glowing borders, glitch-like effects (simulated), and a clean, structured layout reminiscent of futuristic interfaces.
*   **Naming**: "Master Agentic AI," "Neo-Cognito Hub" (implied), "Synth-Mind Core" (implied).

## Project Structure

```
master-agentic-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application, API endpoints
│   │   ├── config.py               # API key management
│   │   ├── models.py               # Pydantic models for requests/responses
│   │   ├── constitution.py         # The AI's ethical constitution
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py       # Base class for all agents
│   │   │   ├── master_orchestrator.py # The Super Agent
│   │   │   ├── planning_agent.py   # Handles task decomposition and planning
│   │   │   ├── execution_agent.py  # Handles tool execution (ReAct)
│   │   │   ├── ethics_agent.py     # Handles ethical review (Constitutional AI)
│   │   │   └── agent_manager.py    # Manages agent instances
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── tool_registry.py    # Registers and provides tools
│   │   │   ├── web_search.py       # Simulated web search tool
│   │   │   ├── code_interpreter.py # Simulated code interpreter tool
│   │   │   └── constitution_retriever.py # Tool to retrieve constitution principles
│   │   └── static/                 # Frontend build files will be served from here
│   ├── .env.example                # Example environment variables
│   ├── Dockerfile                  # Dockerfile for the backend
│   └── requirements.txt            # Python dependencies
├── frontend/
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── assets/
│   │   │   └── react.svg
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx      # Displays chat messages
│   │   │   ├── Message.jsx         # Individual chat message component
│   │   │   ├── InputBar.jsx        # User input field
│   │   │   └── SettingsModal.jsx   # Modal for API key input
│   │   ├── App.jsx                 # Main React component
│   │   ├── index.css               # Tailwind CSS imports and custom styles
│   │   └── main.jsx                # React entry point
│   ├── .env.example                # Example environment variables for frontend (not used for API key)
│   ├── index.html                  # HTML entry point
│   ├── package.json                # Node.js dependencies
│   ├── postcss.config.js           # PostCSS configuration for Tailwind
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   └── vite.config.js              # Vite configuration
├── .dockerignore
├── docker-compose.yml              # Docker Compose file for both services
└── README.md                       # Project README
```

## Installation and Setup

### Prerequisites

*   Docker Desktop (includes Docker Engine and Docker Compose)
*   Node.js and npm (if running frontend outside Docker for development)
*   Python 3.9+ and pip (if running backend outside Docker for development)

### Step-by-Step Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/master-agentic-ai.git
    cd master-agentic-ai
    ```

2.  **Backend Setup:**
    *   Navigate to the `backend` directory:
        ```bash
        cd backend
        ```
    *   Create a `.env` file by copying `.env.example`:
        ```bash
        cp .env.example .env
        ```
    *   Open `.env` and add your Gemini API key:
        ```
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
        ```
        *Note: While the application allows user insertion, this key will be used as a fallback or for initial testing if not provided via the UI.*

3.  **Frontend Setup (Optional - for local development without Docker):**
    *   Navigate to the `frontend` directory:
        ```bash
        cd ../frontend
        ```
    *   Install dependencies:
        ```bash
        npm install
        ```

4.  **Build and Run with Docker Compose (Recommended):**
    *   Go back to the root directory of the project:
        ```bash
        cd ..
        ```
    *   Build the Docker images and start the services:
        ```bash
        docker-compose up --build
        ```
    *   This will:
        *   Build the `frontend` image (which then copies its build output to the `backend/app/static` directory).
        *   Build the `backend` image.
        *   Start both the backend (FastAPI) and frontend (served by FastAPI) services.

5.  **Access the Application:**
    *   Once Docker Compose is up, open your web browser and go to: `http://localhost:8000`
    *   You will see the Master Agentic AI interface.
    *   **Important**: Before interacting, click the "Settings" icon (gear) in the top right corner and **paste your Gemini API Key** into the input field. This key will be used for all subsequent AI interactions.

### Running Locally (without Docker - for development)

**Backend:**

1.  Navigate to `backend/`.
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    The backend will be available at `http://localhost:8000`.

**Frontend:**

1.  Navigate to `frontend/`.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173` (or another port Vite assigns).
    *Note: When running frontend and backend separately, you might need to adjust the API base URL in `frontend/src/App.jsx` if the backend is not on `http://localhost:8000`.*

## Usage

1.  **Set Gemini API Key**: Upon loading the application, click the "Settings" icon (gear) in the top right corner. Enter your Gemini API key and click "Save." This key is stored in your browser's session storage and sent with each request to the backend.
2.  **Interact with the Master Agent**: Type your queries into the input bar at the bottom of the screen and press Enter or click the "Send" button.
3.  **Observe Agent Activity**: The chat window will display messages indicating which agent is active (e.g., "Orchestrator thinking...", "Planning Agent active...", "Executing tool: web_search..."). This provides transparency into the MAS's internal workings.
4.  **Ethical Responses**: Test the `EthicsAgent` by asking for harmful or unethical content. The agent should politely decline and explain its reasoning, offering ethical alternatives.

## Code Explanation

### Backend (`backend/app/`)

*   **`main.py`**:
    *   Initializes the FastAPI app.
    *   Sets up CORS middleware to allow frontend requests.
    *   Defines the `/set-api-key` endpoint to receive and store the user's Gemini API key in the `config` module.
    *   Defines the `/chat` endpoint:
        *   Receives user messages.
        *   Retrieves the Gemini API key.
        *   Initializes the `MasterAgentOrchestrator` with the API key.
        *   Calls the orchestrator's `handle_message` method.
        *   Streams agent activity and final responses back to the frontend.
    *   Serves static files (the built React frontend) from the `/static` directory.
*   **`config.py`**: A simple module to hold the `GEMINI_API_KEY` dynamically. In a production environment, this would be more robust (e.g., using a database or secure vault).
*   **`models.py`**: Pydantic models for `ChatRequest`, `ChatResponse`, and `ApiKeyRequest` to ensure data integrity for API communication.
*   **`constitution.py`**: Contains a multi-line string representing the "Constitution" for the `EthicsAgent`. This is a simplified representation of the ethical principles from the blueprint.
*   **`agents/`**:
    *   **`base_agent.py`**: Defines a `BaseAgent` class with common methods like `_get_gemini_model` and `_generate_content`. All other agents inherit from this.
    *   **`agent_manager.py`**: A simple class to manage the lifecycle of agent instances, ensuring they are initialized with the correct API key.
    *   **`master_orchestrator.py`**:
        *   The central brain. Its `handle_message` method orchestrates the entire process:
            1.  Sends a "thinking" message.
            2.  Calls `PlanningAgent` to get a plan.
            3.  Calls `EthicsAgent` to review the plan. If rejected, it tries to revise or declines.
            4.  Iterates through the plan, calling `ExecutionAgent` for each step.
            5.  Synthesizes the final response.
            6.  Handles conversation history.
    *   **`planning_agent.py`**:
        *   Its `plan_task` method takes a goal and uses Gemini to generate a structured plan (list of steps). The prompt emphasizes CoT.
    *   **`execution_agent.py`**:
        *   Its `execute_step` method takes a single step from the plan.
        *   It uses a ReAct-style prompt to guide Gemini to `Thought`, `Action` (using a tool), and `Observation`.
        *   It parses the tool calls and executes them via the `ToolRegistry`.
    *   **`ethics_agent.py`**:
        *   Its `review_plan_or_output` method takes a plan/output.
        *   It uses the `constitution_retriever` tool to "retrieve" relevant principles.
        *   It prompts Gemini to critique the input against these principles, suggesting revisions or declining if harmful.
*   **`tools/`**:
    *   **`tool_registry.py`**: A simple class that maps tool names (e.g., "web_search") to their corresponding Python functions.
    *   **`web_search.py`**: A mock function that simulates a web search. In a real application, this would integrate with a search API (e.g., Google Search API, SerpAPI).
    *   **`code_interpreter.py`**: A mock function that simulates code execution. In a real application, this would involve a secure sandboxed environment.
    *   **`constitution_retriever.py`**: A mock function that simply returns the entire `constitution.py` content. In a real RAG system, this would query a vector database based on the input query.

### Frontend (`frontend/src/`)

*   **`main.jsx`**: The entry point for the React application.
*   **`index.css`**: Imports Tailwind CSS and defines custom cyberpunk-themed styles (colors, fonts, basic layout).
*   **`App.jsx`**:
    *   Manages the main application state: `messages`, `isLoading`, `apiKey`.
    *   Handles sending messages to the backend and receiving streamed responses.
    *   Manages the `SettingsModal` for API key input.
    *   Renders the `ChatWindow`, `InputBar`, and `SettingsModal` components.
*   **`components/`**:
    *   **`ChatWindow.jsx`**: Displays all chat messages, scrolling to the bottom automatically.
    *   **`Message.jsx`**: Renders a single chat message, distinguishing between user and AI messages.
    *   **`InputBar.jsx`**: Contains the text input field and send button.
    *   **`SettingsModal.jsx`**: A modal dialog for users to input and save their Gemini API key. The key is stored in `sessionStorage` for persistence within the session.

## Deployment Instructions

The provided `docker-compose.yml` is set up for easy local deployment. For production deployment, you would typically:

1.  **Build Frontend**: Run `npm run build` in the `frontend` directory. This creates a `dist` folder.
2.  **Copy Frontend to Backend**: Copy the contents of `frontend/dist` to `backend/app/static`.
3.  **Build Backend Docker Image**:
    ```bash
    cd backend
    docker build -t master-agentic-ai-backend .
    ```
4.  **Deploy Backend**: Push the `master-agentic-ai-backend` image to a container registry (e.g., Docker Hub, Google Container Registry, AWS ECR). Then, deploy it to a cloud platform (e.g., Google Cloud Run, AWS ECS, Kubernetes) ensuring environment variables (`GEMINI_API_KEY`) are securely managed.
5.  **HTTPS**: For production, always use HTTPS to encrypt communication. This typically involves setting up a reverse proxy (like Nginx or Caddy) or using your cloud provider's load balancer/gateway.

This comprehensive setup provides a robust foundation for the Master Agentic AI, demonstrating the power of multi-agent systems and ethical AI principles in a practical application.

## Continuous Integration

A GitHub Actions workflow validates the project on every push and pull request by compiling the backend and running frontend lint/build steps. See [WORKFLOWS.md](WORKFLOWS.md) for the exact commands and how to run them locally.
