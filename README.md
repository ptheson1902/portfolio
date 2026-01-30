# PHAM THE SON - Portfolio

Production-ready portfolio website optimized for job applications in:
- Engineering Leader
- BrSE (Bridge Software Engineer)
- Fullstack Engineer

## Features

- **Role-based content**: Adapts presentation based on selected job role
- **Multi-language**: Japanese, Vietnamese, English
- **AI Chat**: Answer questions based on skill sheet data
- **Dark/Light mode**: Toggle between themes
- **Responsive**: Mobile-first design

## Tech Stack

### Backend
- Python + FastAPI
- Role-aware API responses
- OpenAI integration for AI chat

### Frontend
- React + TypeScript
- Tailwind CSS
- Framer Motion
- i18next for internationalization

## Quick Start

### Development

1. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI API key
uvicorn app.main:app --reload
```

2. **Frontend**
```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
# Production
docker-compose up -d

# Development with hot reload
docker-compose -f docker-compose.dev.yml up
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile?lang=&role=` | Get profile data |
| GET | `/api/skills?lang=&role=` | Get skills data |
| GET | `/api/projects?lang=&role=` | Get projects data |
| POST | `/api/chat` | AI chat endpoint |

### Parameters
- `lang`: `ja`, `vi`, `en`
- `role`: `leader`, `brse`, `fullstack`

### Chat Request Body
```json
{
  "question": "string",
  "lang": "ja",
  "role": "fullstack",
  "mode": "single"
}
```

## Project Structure

```
portfolio/
├── backend/
│   ├── app/
│   │   ├── models/       # Pydantic schemas
│   │   ├── routers/      # API routes
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── context/      # App context
│   │   ├── hooks/        # Custom hooks
│   │   ├── i18n/         # Translations
│   │   ├── pages/        # Page sections
│   │   └── types/        # TypeScript types
│   ├── Dockerfile
│   └── package.json
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── docker-compose.dev.yml
```

## Environment Variables

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Deployment

### AWS / Azure / VPS

1. Copy files to server
2. Create `.env` files with production values
3. Run `docker-compose up -d`
4. Configure domain and SSL with reverse proxy

## License

MIT
