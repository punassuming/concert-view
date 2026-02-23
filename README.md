# Concert View

A framework for ingesting multiple video feeds of the same live experience (concerts, events) and composing them into a dynamic multi-angle collage with synchronized audio.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Frontend   │────▶│   API (Fast   │────▶│   Processor     │
│  (React/Vite)│◀────│    API)      │◀────│  (FFmpeg/NumPy) │
│  Port 3000   │     │  Port 8000   │     │                 │
└─────────────┘     └──────────────┘     └─────────────────┘
                           │
                    ┌──────┴──────┐
                    │  AI Service  │
                    │ (OpenAI /    │
                    │  Gemini)     │
                    └─────────────┘
```

**Services:**

| Service | Technology | Purpose |
|---------|-----------|---------|
| `api` | Python / FastAPI | REST API for feed, layout, and audio management |
| `processor` | Python / FFmpeg / NumPy | Video composition, audio sync, and optimization |
| `frontend` | React / Vite | Dashboard UI for managing feeds, layouts, and audio |

## Features

- **Feed Management** – Register, upload, and manage multiple video feeds
- **Layout Editor** – Visual layout editor with grid and picture-in-picture presets
- **AI-Assisted Layout** – Optional AI suggestions for dynamic layouts (OpenAI / Gemini)
- **Audio Synchronization** – Cross-correlation-based offset detection between feeds
- **Audio Optimization** – Loudness normalization and noise reduction via FFmpeg
- **Video Composition** – Compose multiple feeds into a single output using FFmpeg filter graphs
- **Docker Compose** – Full stack orchestration with a single command

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Run with Docker

```bash
# Copy and configure environment variables (optional - AI features)
cp .env.example .env
# Edit .env to add OPENAI_API_KEY or GEMINI_API_KEY if desired

# Start all services
docker compose up --build
```

The services will be available at:
- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Local Development

**API:**
```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Processor:**
```bash
cd processor
pip install -r requirements.txt
python -m processor.main
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Testing

```bash
# API tests
cd api && python -m pytest app/tests/ -v

# Processor tests
cd processor && python -m pytest tests/ -v
```

## API Endpoints

### Feeds
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feeds` | List all feeds |
| POST | `/api/feeds` | Register a new feed |
| GET | `/api/feeds/{id}` | Get feed details |
| PATCH | `/api/feeds/{id}` | Update feed settings |
| DELETE | `/api/feeds/{id}` | Remove a feed |
| POST | `/api/feeds/{id}/upload` | Upload video file |

### Layouts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/layouts` | List all layouts |
| POST | `/api/layouts` | Create a layout |
| GET | `/api/layouts/{id}` | Get layout details |
| PATCH | `/api/layouts/{id}` | Update a layout |
| DELETE | `/api/layouts/{id}` | Remove a layout |
| POST | `/api/layouts/suggest` | AI-assisted layout suggestion |

### Audio
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/audio/sync` | Analyze audio sync across feeds |
| POST | `/api/audio/optimize` | Optimize audio output |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | _(empty)_ | OpenAI API key for AI layout suggestions |
| `GEMINI_API_KEY` | _(empty)_ | Google Gemini API key (fallback if no OpenAI key) |
| `UPLOAD_DIR` | `/data/uploads` | Directory for uploaded video files |
| `OUTPUT_DIR` | `/data/output` | Directory for composed output files |

## License

MIT
