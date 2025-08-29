# Fact Guard

A lightweight, local-first fact-checking assistant for individuals. Submit claims, URLs, or documents (PDF/CSV) and receive verdicts (True/False/Unclear) with confidence scores and supporting evidence from trusted sources.

## Features

- **Multi-input Support**: Submit text claims, URLs, or upload PDF/CSV documents
- **Local LLM Processing**: Uses Ollama for private, offline fact-checking
- **Vector Search**: Semantic search through your document library using Qdrant
- **Async Processing**: Background job system for handling long-running operations  
- **Modern UI**: React-based interface with real-time job status updates

## Architecture

- **Backend**: FastAPI (Python) with async job processing
- **Frontend**: React (TypeScript) with Vite and styled-components
- **LLM**: Ollama for local language model inference
- **Vector DB**: Qdrant for semantic document search
- **Embeddings**: FastEmbed for efficient text embeddings

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)

### Docker Development (Recommended)

Start all services with Docker Compose:

```bash
docker-compose up
```

This starts:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Qdrant: http://localhost:6333
- Ollama: http://localhost:11434

### Local Development

#### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend (React + Vite)

```bash
cd ui
npm install
npm run dev
```

## API Endpoints

- `POST /api/check` - Submit fact-checking requests
- `POST /api/upload` - Upload documents for processing
- `GET /api/jobs/{job_id}` - Check job status
- `GET /api/library` - Manage document library

## Development

### Code Quality

**Backend:**
```bash
cd backend
black app/          # Format code
isort app/          # Sort imports
flake8 app/         # Lint
mypy app/          # Type checking
pytest             # Run tests
```

**Frontend:**
```bash
cd ui
npm run lint       # ESLint
npm run type-check # TypeScript checking
npm run build      # Production build
```

### Project Structure

```
fact-guard/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/      # API route handlers
│   │   ├── core/     # Core business logic
│   │   ├── models/   # Pydantic models
│   │   ├── services/ # Service layer
│   │   └── utils/    # Utilities
│   └── requirements.txt
├── ui/               # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/      # Custom hooks
│   │   ├── services/   # API clients
│   │   └── types/      # TypeScript types
│   └── package.json
└── docker-compose.yml
```

## Key Dependencies

**Backend:**
- FastAPI - Web framework
- Ollama - LLM integration
- Qdrant Client - Vector database
- FastEmbed - Text embeddings
- Docling - Document processing
- Pydantic - Data validation

**Frontend:**
- React 19 - UI framework
- TypeScript - Type safety
- Vite - Build tool
- Styled Components - CSS-in-JS
- Framer Motion - Animations
- Lucide React - Icons

## Configuration

Backend configuration via environment variables (`.env` file supported):

```env
OLLAMA_BASE_URL=http://localhost:11434
QDRANT_HOST=localhost
QDRANT_PORT=6333
DEBUG=true
```

## Data Flow

1. User submits claim/URL/document via React UI
2. Backend creates async job and returns `job_id`
3. Background worker processes request using LLM and vector search
4. Frontend polls job status and displays results
5. Results include verdict, confidence score, and evidence sources

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Follow existing code style and conventions
2. Use async/await patterns for backend operations
3. Maintain TypeScript type safety
4. Test locally with Docker Compose before submitting

---

Built with ❤️ for transparent, local fact-checking.