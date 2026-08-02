# AutoDev AI - Autonomous Multi-Agent Software Engineering Team

An autonomous AI platform where 9 specialized AI agents collaborate like a real software development team to turn a plain-English idea into working code, a database schema, tests, documentation, and deployment configuration - end to end, with self-correction built in.

**Live demo**: https://autodev-ai-nine.vercel.app
**Backend API docs**: https://autodev-backend-kmg1.onrender.com/docs

> Note: the backend runs on a free-tier server that sleeps after inactivity. The first request may take 30-60 seconds to respond while it wakes up.

---

## What it does

Give it an idea like "Build an expense tracker with authentication and monthly reports" and the AI team:

1. Converts the idea into structured requirements
2. Designs a system architecture (frontend/backend/database choices)
3. Generates a PostgreSQL schema
4. Generates backend (FastAPI) code
5. Generates frontend (React + TypeScript) code
6. Reviews the generated code for bugs and security issues
7. Tests the generated code
8. If tests fail, automatically sends the code back for a fix and re-tests (self-healing loop)
9. Writes a README for the generated project
10. Generates Docker deployment configuration

The result is downloadable as a ZIP - real, runnable files, not just a chat response.

---

## Architecture

```
React Frontend (Vercel)
        |
FastAPI Backend (Render)
        |
LangGraph Supervisor Agent
        |
   --------------------------------------------------
   Product | Architect | Database | Backend Dev
   Frontend Dev | Reviewer | Testing | Docs | DevOps
   --------------------------------------------------
        |
PostgreSQL (Render) + ChromaDB (RAG knowledge base)
        |
Groq (Llama 3.3 70B) for all agent reasoning
```

**Orchestration**: LangGraph `StateGraph` with a Supervisor pattern. The Supervisor inspects shared state after every agent runs and decides what happens next - including routing failed code back to the Backend Dev agent when Testing fails, capped at one retry to avoid infinite loops.

**Reliability engineering**:
- LLM output is validated against actual state before being trusted (the Supervisor's routing decision is double-checked by code, not blindly followed)
- Retry-with-backoff on LLM API rate limits
- Marker-based file parsing instead of JSON-embedded code strings, to avoid JSON-escaping failures on multi-line source code

**RAG**: Backend, Frontend, and Database agents retrieve relevant best-practice snippets from a ChromaDB knowledge base before generating code, grounding output rather than relying purely on the LLM's training data.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS, React Router, React Query |
| Backend | FastAPI, SQLAlchemy, Pydantic, Alembic, JWT auth |
| AI orchestration | LangGraph, LangChain, Groq (Llama 3.3 70B) |
| Vector store | ChromaDB |
| Database | PostgreSQL |
| Deployment | Docker, Docker Compose, Render, Vercel |

---

## Project structure

```
autodev-ai/
+-- backend/
|   +-- app/            FastAPI app: routes, models, schemas, services, repositories
|   +-- agents/         The 9 AI agents + Supervisor
|   +-- graphs/         LangGraph state schema, routing, graph assembly
|   +-- tools/          RAG retriever
|   +-- alembic/        Database migrations
+-- frontend/
|   +-- src/
|       +-- pages/       Login, Register, Dashboard, ProjectDetails, Profile, etc.
|       +-- components/  Navbar, PipelineStrip, ProtectedRoute
|       +-- api/         Backend API client
+-- vectorstore/         RAG knowledge base ingestion
+-- docker-compose.yml
+-- generated_projects/  Output folder for AI-generated code
```

---

## Running it locally

### Prerequisites
- Docker Desktop
- A free Groq API key from console.groq.com

### Steps

1. Clone the repo:
```
git clone https://github.com/skshaheen07/autodev-ai.git
cd autodev-ai
```

2. Create a .env file in the project root (see .env.example):
```
GROQ_API_KEY=your_key_here
```

3. Start everything:
```
docker-compose up --build
```

4. Open http://localhost:5174

---

## Key features

- 9 specialized AI agents, each with a distinct role and system prompt
- Self-healing retry loop: agents retry on empty/malformed output; the Supervisor routes failed code back to the Dev agent when tests fail, with a bounded retry count
- RAG-grounded code generation using ChromaDB
- JWT authentication with bcrypt password hashing, forgot/reset password flow
- Live progress tracking - React Query polling shows pipeline status in real time
- Downloadable output - every generated project is written to disk and available as a ZIP
- Fully containerized - one docker-compose up runs the entire stack
- Deployed and publicly accessible - not just a local demo

---

## Author

Built by Shaik Shaheen Tabassum.