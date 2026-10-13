# Multi-Sport Game Video Analyst & Coach

A conversational sports analysis and coaching agent built with Google Agent Development Kit (ADK) and Gemini. The agent analyzes gameplay technique across sports (Badminton, Cricket, Field Hockey), diagnoses mechanics, prescribes targeted training drills, retrieves historical analysis reports, and illustrates tactical adjustments with generated imagery.

![Multi-Sport Game Video Analyst Demo](demo.gif)

---

## What the Agent Does

- **Kinematic & Technique Breakdown**: Diagnoses athletic technique from gameplay observations (e.g. smash approach footwork, batting backlift, drag flick follow-through) and structures actionable coaching drills.
- **Cross-Session Athlete Memory**: Automatically tracks user preferences, skill level, recurring technical weaknesses, and training history across sessions using Vertex AI Memory Bank.
- **Persistent Match & Analysis Storage**: Queries and records player analysis reports, scores, and coaching notes directly in Google Cloud Firestore.
- **Domain Playbook & Pro Profiles**: Retrieves training drills and benchmark athlete profiles (Viktor Axelsen, Virat Kohli, Manpreet Singh) via structured database lookups.
- **Tactical Diagram Generation**: Synthesizes custom tactical stance and positioning diagrams using Imagen / Gemini Image Generation (`gemini-3.1-flash-lite-image`), uploads them to Google Cloud Storage, and attaches them to session artifacts.
- **Video Demonstration Clip Generation**: Generates short motion clips demonstrating gameplay technique using Google's Omni model (`gemini-omni-flash-preview`) in the global region and uploads them directly to Google Cloud Storage.
- **Sandboxed Statistical Computation**: Executes performance metric calculations (strike rates, shot distribution percentages, conversion rates) securely inside an Agent Engine Sandbox environment.
- **A2UI Rich Card Rendering**: Returns structured cards with headings, body text, and embedded diagrams adhering to A2UI v0.8 specifications.

---

## Implemented Architecture & Google Cloud Services

| Capability | Component / Service | Implementation Details |
|---|---|---|
| **Core LLM** | Gemini 3.8 Flash (`gemini-3.8-flash`) | ADK `root_agent` reasoning engine |
| **Long-Term Memory** | Vertex AI Memory Bank | `PreloadMemoryTool` + `generate_memories_callback` (`add_session_to_memory`) |
| **Database Storage** | Google Cloud Firestore | `list_analysis_reports`, `get_analysis_report`, `save_analysis_report`, `lookup_training_playbook`, `fetch_pro_athlete_profile` |
| **Asset Storage** | Google Cloud Storage (GCS) | Media uploads for tactical diagrams and video clips |
| **Tactical Image Generation** | Gemini Image Generation (`gemini-3.1-flash-lite-image`) | `generate_tactical_diagram` tool with GCS upload and session artifact storage |
| **Video Motion Generation** | Google Omni (`gemini-omni-flash-preview`) | `generate_sports_video` tool via global Vertex AI Interactions API |
| **Code Sandbox** | Agent Engine Sandbox | `AgentEngineSandboxCodeExecutor` for calculating metrics and stats |
| **Rich UI Surfaces** | A2UI (v0.8 Basic Catalog) | `A2uiSchemaManager` with `a2ui_callback` after-model hook |
| **Interoperability** | A2A Protocol (Agent-to-Agent) | FastA2A / A2A 1.0 streaming client proxy |

> [!NOTE]
> **Planned / Future Features**: Automated computer vision frame extraction directly from user-uploaded raw video files (currently sports video descriptions and metrics are evaluated via agent reasoning and multimodal prompt analysis).

---

## Project Structure

```
sports-video-analyst/
├── app/
│   ├── agent.py               # Core ADK agent, tools, callbacks, and A2UI schema
│   ├── a2ui_utils.py          # A2UI callback and JSON validation handler
│   ├── fast_api_app.py        # FastAPI A2A backend service
│   └── app_utils/             # Shared helpers and types
├── frontend/
│   ├── main.py                # FastAPI proxy connecting browser to deployed agent over A2A
│   ├── static/
│   │   └── index.html         # Athletic themed chat UI with dialogue layout & example chips
│   ├── Dockerfile             # Container definition for frontend
│   └── requirements.txt       # Frontend dependencies (a2a-sdk, fastapi, uvicorn)
├── demo.gif                   # Looping preview recording of the agent in action
├── seed_data.py               # Firestore database seeder with playbooks, reports & pro profiles
├── pyproject.toml             # Python dependencies managed with uv
└── agents-cli-manifest.yaml   # Agent deployment manifest
```

---

## Local Setup and Running

### 1. Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (`gcloud`) authenticated to your Google Cloud project

### 2. Install Dependencies

```bash
uv sync
```

### 3. Authenticate with Google Cloud

Ensure application default credentials and project configuration are active:

```bash
gcloud auth application-default login
gcloud config set project <YOUR_PROJECT_ID>
```

### 4. Seed Firestore Database

Initialize the sample playbooks, pro athlete profiles, and initial analysis reports:

```bash
uv run python3 seed_data.py
```

### 5. Launch Local ADK Web Playground

To launch the ADK development web interface with cross-session Memory Bank connected:

```bash
uv run adk web . --port 8080 --reload_agents --memory_service_uri=agentengine://<YOUR_MEMORY_BANK_ID>
```

### 6. Run the Custom Chat Frontend

In a separate terminal, launch the custom themed web frontend:

```bash
cd frontend
uv run uvicorn main:app --host 0.0.0.0 --port 3000
```
