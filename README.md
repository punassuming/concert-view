# Concert View

A single-workstation video curation and editing tool for merging multiple concert camera feeds into a cohesive, polished video. Ingest recorded video files from different angles, synchronize audio, arrange clips on a timeline, compose multi-angle layouts, and export a finished video ready for social media.

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
| `api` | Python / FastAPI | REST API for clip, layout, project, and audio management |
| `processor` | Python / FFmpeg / NumPy | Video composition, timeline rendering, audio sync, optimization, and social media export |
| `frontend` | React / Vite | Dashboard UI for managing clips, layouts, projects, audio, and export |

## Features

- **Clip Management** – Register and upload local video files from multiple cameras/angles; set per-clip trim points (in/out), volume, and sync offset
- **Layout Editor** – Visual multi-angle layout editor with grid and picture-in-picture presets
- **AI-Assisted Layout** – Optional AI suggestions for dynamic layouts (OpenAI / Gemini)
- **Audio Synchronization** – Cross-correlation-based offset detection between recorded clips
- **Audio Optimization** – Loudness normalization and noise reduction via FFmpeg
- **Video Composition** – Compose multiple clips side-by-side into a single output using FFmpeg filter graphs
- **Timeline / Project** – Sequence clips in order on a project timeline; trim and arrange them to build the final concert video
- **Social Media Export** – One-click export to platform-ready formats: Landscape 1080p (16:9) for YouTube, Portrait 1080p (9:16) for TikTok/Reels/Shorts, and Square 1080 (1:1) for Instagram
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

### Clips (Feeds)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feeds` | List all clips |
| POST | `/api/feeds` | Register a new clip |
| GET | `/api/feeds/{id}` | Get clip details |
| PATCH | `/api/feeds/{id}` | Update clip settings (trim, volume, offset) |
| DELETE | `/api/feeds/{id}` | Remove a clip |
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

### Projects (Timeline)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Create a new project |
| GET | `/api/projects/{id}` | Get project details |
| PATCH | `/api/projects/{id}` | Update project clips/settings |
| DELETE | `/api/projects/{id}` | Remove a project |
| POST | `/api/projects/{id}/render` | Render project timeline to video file |

### Audio
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/audio/sync` | Analyze audio sync across clips |
| POST | `/api/audio/optimize` | Optimize audio output |

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/{id}` | Get job status and result |
| POST | `/api/jobs/compose` | Compose multi-angle layout to video |
| POST | `/api/jobs/sync` | Detect audio offset between two files |
| POST | `/api/jobs/optimize` | Optimize audio of a file |
| POST | `/api/jobs/export` | Export video to social media format |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | _(empty)_ | OpenAI API key for AI layout suggestions |
| `GEMINI_API_KEY` | _(empty)_ | Google Gemini API key (fallback if no OpenAI key) |
| `UPLOAD_DIR` | `/data/uploads` | Directory for uploaded video files |
| `OUTPUT_DIR` | `/data/output` | Directory for composed output files |

## License

MIT
