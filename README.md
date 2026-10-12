# SmartStudy: Multi-Agent Intelligent Study Planner

Built for the **Google Agent Development Kit (ADK) Workshop Certification Assignment — Task 2** (40 Marks).

---

## 1. Project Overview

**SmartStudy** is a production-grade multi-agent study planning system designed to eliminate the struggle students face when allocating finite study time across complex syllabi. Rather than operating as a naive single-turn LLM chatbot, SmartStudy coordinates **seven specialized agents** organized into real Google ADK workflows: **Sequential**, **Parallel**, and a **Bounded Review Loop**.

The system ingests a student's exam deadline, proficiency level, topic list, and daily availability, normalizes these constraints, computes topic difficulties and practice problem targets concurrently, drafts an hourly schedule, and audits the result against five rigorous quality criteria before presenting the verified plan.

---

## 2. Multi-Agent Architecture & Workflows

SmartStudy leverages Google ADK 2.11.0 workflow primitives:

```
User Request
     │
     ▼
[ Coordinator Agent ]         (Sequential Stage 1: Extracts & normalizes inputs)
     │
     ▼
[ Planning Agent ]            (Sequential Stage 2: Formulates strategic brief)
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  ParallelAgent: Specialist Analysts                         │
│  ├─ [ Topic Agent ]      ──► topic_analysis                 │
│  ├─ [ Practice Agent ]   ──► practice_plan                  │
│  └─ [ Schedule Agent ]   ──► schedule_plan                  │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  LoopAgent: Bounded Refinement (max_iterations = 2)         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  1. [ Study Plan Writer Agent ] ──► draft_plan        │  │
│  │                    │                                  │  │
│  │                    ▼                                  │  │
│  │  2. [ Review Agent ]            ──► review_feedback   │  │
│  │       ├─ If Approved: calls exit_loop tool ───────────────┼──► [Exit Loop]
│  │       └─ If Issues: routes feedback back to Writer    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
[ Final Response Agent ]      (Sequential Stage 5: Formats definitive plan)
     │
     ▼
Verified 10-Day Study Blueprint
```

---

## 3. Seven Agent Roles & State Output Contracts

Every agent writes to an isolated, explicit session state key to prevent overwrites and enable coordinated data flow:

| # | Agent Role | ADK Workflow | Output Key | Primary Responsibility |
|---|---|---|---|---|
| 1 | **Coordinator Agent** | Sequential | `student_requirements` | Normalizes input into structured subject, deadline, topics, level, and hours/day. |
| 2 | **Planning Agent** | Sequential | `planning_brief` | Calculates total study budget ($10 \times 3\text{h} = 30\text{h}$) and sets pacing guidelines. |
| 3 | **Topic Agent** | Parallel | `topic_analysis` | Evaluates priority (High/Med/Low), difficulty, learning focus, and duration per topic. |
| 4 | **Practice Agent** | Parallel | `practice_plan` | Calibrates problem counts (4–8/topic), practice types (coding vs concepts), and pedagogical rationales. |
| 5 | **Schedule Agent** | Parallel | `schedule_plan` | Constructs daily hourly distributions strictly $\le \text{hours\_per\_day}$, adding spaced revision and final mock prep. |
| 6 | **Study Plan Writer** | Loop | `draft_plan` | Synthesizes specialist outputs and incorporates reviewer feedback into complete day cards. |
| 7 | **Review Agent** | Loop | `review_feedback` | Audits the draft against all 5 quality criteria; triggers `exit_loop` upon approval. |
| 8 | **Final Response Agent** | Sequential | `final_plan` | Assembles verification badges, metrics, breakdown tables, and day cards in Markdown. |

---

## 4. Bounded Review Loop & Quality Criteria

The `LoopAgent` is capped at **2 iterations maximum** and enforces five non-negotiable criteria:

1. **Topic Coverage:** Every topic from the syllabus (Arrays, Linked Lists, Trees, Graphs, DP) must be present.
2. **Time Constraint Enforcement:** Every single day's total duration must be strictly $\le \text{hours\_per\_day}$ (no day exceeds 3.0h).
3. **Sufficient Practice:** Dedicated coding and algorithmic problem counts tailored to student proficiency.
4. **Spaced Revision:** Daily active recall prompts distributed throughout the schedule rather than deferred to the end.
5. **Final Day Readiness:** The final day is reserved for timed mock exam simulation, formula review, and confidence building.

When all 5 criteria pass, the Reviewer executes `exit_loop`, terminating the loop early. If issues are detected on iteration 1, feedback is injected into the Writer for iteration 2, after which the loop halts automatically.

---

## 5. Project Directory Structure

```text
task2_smartstudy/
├── smartstudy/
│   ├── __init__.py                # Exposes root_agent for ADK loader discovery
│   ├── agent.py                   # Master ADK Sequential, Parallel, and Loop workflow
│   ├── schemas.py                 # Pydantic validation schemas & output contracts
│   └── agents/
│       ├── coordinator.py         # Coordinator Agent (student_requirements)
│       ├── planning.py            # Planning Agent (planning_brief)
│       ├── topic.py               # Topic Agent (topic_analysis)
│       ├── practice.py            # Practice Agent (practice_plan)
│       ├── schedule.py            # Schedule Agent (schedule_plan)
│       ├── writer.py              # Study Plan Writer Agent (draft_plan)
│       ├── reviewer.py            # Review Agent (review_feedback + exit_loop)
│       └── final_response.py      # Final Response Agent (final_plan)
├── frontend/                      # Custom editorial dashboard (React + TS + Vite + Tailwind)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx        # Navigation, syllabus presets, architecture summary
│   │   │   ├── PlannerForm.tsx    # Interactive syllabus & constraint inputs
│   │   │   ├── WorkflowProgress.tsx # Live pipeline tracking (5 ADK stages)
│   │   │   ├── QualityBadge.tsx   # Verification badge for 5 quality criteria
│   │   │   ├── TopicBreakdown.tsx # Topic difficulty & problem intensity cards
│   │   │   ├── DayCard.tsx        # Expandable daily study cards with tasks & revision
│   │   │   └── StudyPlanResults.tsx # Blueprint summary, metrics & Markdown toggle
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── types.ts
│   ├── package.json
│   └── vite.config.ts
├── tests/
│   ├── test_schemas.py            # Pydantic model validation & constraints
│   ├── test_schedule_validation.py # 2h/3h limits, missing topic & revision checks
│   └── test_workflow.py           # Topology, agent roles, loop bounds & output keys
├── assets/
│   ├── adk_web_ui_loaded.png      # Official ADK 2.11 Web UI screenshot
│   ├── smartstudy_frontend_screenshot.png # Custom frontend workspace
│   ├── smartstudy_results_screenshot.png  # Generated 10-day blueprint with review audit
│   └── test_a_response.json       # Live response payload from ADK execution
├── api_server.py                  # FastAPI bridge (/api/health, /api/study-plans)
├── test_a_final_plan.md           # Live generated 10-day Markdown blueprint
├── requirements.txt               # Backend dependencies
├── .env.example                   # Secret-free environment template
├── .gitignore                     # Git rules ensuring secrets remain excluded
└── README.md
```

---

## 6. Setup & Execution Instructions

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Google Gemini API Key from [Google AI Studio](https://aistudio.google.com)

### 2. Configure Environment
```bash
cd task2_smartstudy
cp .env.example .env
```
Edit `.env`:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

### 3. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Automated Test Suite
```bash
pytest tests -v
```
*Expected: 11 passed (covering schemas, schedule constraints, topic coverage, 2h limits, and workflow topology).*

---

## 7. Running the Official ADK Web UI

To launch Google ADK's native Web UI:

```bash
adk web . --port 8085
```
Open **`http://127.0.0.1:8085`** in your browser. Select **`smartstudy`** from the application dropdown.

### Exact Assignment Baseline Test Prompt:
```text
I have a Data Structures exam in 10 days.

My current level is Intermediate.

Topics:
- Arrays
- Linked Lists
- Trees
- Graphs
- Dynamic Programming

I can study for 3 hours per day.

Create a preparation plan for me.
```

The system will execute all 7 agents in sequence, run parallel analysis, execute the writer-reviewer loop, and present the final 10-day study blueprint.

---

## 8. Running the Custom SmartStudy Frontend

To run the custom presentation workspace alongside the ADK workflow:

### Terminal 1: Launch Backend Bridge Server
```bash
python api_server.py
```
*Runs on `http://127.0.0.1:8001` (health endpoint: `http://127.0.0.1:8001/api/health`).*

### Terminal 2: Launch Frontend Workspace
```bash
cd frontend
npm install
npm run dev
```
*Runs on `http://127.0.0.1:5173`.*

---

## 9. Verification & Submission Checklist

- [x] **All 7 Agent Roles Implemented:** Coordinator, Planning, Topic, Practice, Schedule, Writer, Reviewer (+ Final Response Agent).
- [x] **Real ADK Workflows:** `SequentialAgent`, `ParallelAgent`, and `LoopAgent` executed natively.
- [x] **Bounded Review Loop:** Strict `max_iterations = 2` with early termination via `exit_loop`.
- [x] **No State Collisions:** 8 distinct output keys configured across agents.
- [x] **Hard Time Constraints:** Verified daily hour limits never exceed stated availability (all days strictly 3.0h).
- [x] **5 Quality Criteria Evaluated:** Coverage, daily limits, practice targets, spaced revision, and mock exam simulation.
- [x] **Assignment Baseline Test Verified:** 10-day Data Structures plan generated with 38 practice problems across all 5 topics.
- [x] **ADK Web UI Operational:** Native discoverable root agent with SQLite session persistence.
- [x] **Zero Secrets in Repository:** `.env` ignored via `.gitignore`; clean `.env.example` provided.
