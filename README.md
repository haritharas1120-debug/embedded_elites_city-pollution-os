# AI-Based Intelligent Air Pollution Monitoring & Intervention System for Chennai

## Overview
This is a production-quality enterprise SaaS dashboard for monitoring air pollution in Chennai. It features real-time data visualization, historical analysis, and a powerful AI multi-agent pipeline that identifies pollution sources and simulates the impact of interventions.

## Architecture
- **Frontend**: Next.js 15 (React 19), Tailwind CSS v4, shadcn/ui, Framer Motion, Recharts, React-Leaflet
- **Backend**: FastAPI (Python), SQLAlchemy, PostgreSQL, Redis, Celery
- **AI Engine**: OpenAI API (Multi-Agent System)
- **Deployment**: Docker & Docker Compose

## Prerequisites
- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)
- OpenAI API Key

## Quick Start (Docker)
The easiest way to run the entire system is using Docker Compose.

1. **Set Environment Variables**:
   In the `backend` directory, create a `.env` file or export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-openai-key-here"
   ```

2. **Run Docker Compose**:
   From the root directory of the project:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:
   - Frontend Dashboard: `http://localhost:3000`
   - Backend API Docs (Swagger): `http://localhost:8000/docs`

## Features Implemented
- [x] **Premium UI**: Glassmorphism, animations, dark mode, responsive design.
- [x] **Live Data Simulation**: Seeder script generates realistic Chennai zones and historical data.
- [x] **Interactive Map**: Leaflet integration for geographical visualization.
- [x] **AI Source Intelligence Agent**: Analyzes telemetry to identify pollution sources.
- [x] **AI Intervention Optimizer**: Recommends prioritized actions.
- [x] **AI Simulator**: Predicts future AQI and pollutant reductions based on selected interventions.
- [x] **Historical Reports**: Exportable CSV data.

## Project Structure
- `/backend`: FastAPI service, models, AI agents, Celery worker.
- `/frontend`: Next.js 15 app router, shadcn/ui components, Zustand store.

## Author
Developed as an advanced AI demonstration project.
