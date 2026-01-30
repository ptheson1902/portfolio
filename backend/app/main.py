"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database.connection import init_db
from .routers import profile_router, skills_router, projects_router, chat_router, auth_router, export_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - initialize database on startup."""
    # Initialize database tables
    init_db()
    print("Database initialized")
    yield
    # Cleanup (if needed)


app = FastAPI(
    title=settings.app_name,
    description="Portfolio API - Role-aware responses for Engineering Leader, BrSE, and Fullstack Engineer positions. Now with database storage and admin CRUD operations.",
    version="2.0.0",
    lifespan=lifespan
)

origins = settings.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public endpoints
app.include_router(profile_router)
app.include_router(skills_router)
app.include_router(projects_router)
app.include_router(chat_router)

# Auth endpoint
app.include_router(auth_router)

# Export endpoint
app.include_router(export_router)


@app.get("/")
async def root():
    return {
        "message": "Portfolio API",
        "version": "2.0.0",
        "features": [
            "SQLite database storage",
            "Role-based access control (RBAC)",
            "Admin CRUD operations",
            "AI-powered chat (reads from database)"
        ],
        "endpoints": {
            "public": {
                "profile": "GET /api/profile?lang=ja&role=fullstack",
                "skills": "GET /api/skills?lang=ja&role=fullstack",
                "projects": "GET /api/projects?lang=ja&role=fullstack",
                "chat": "POST /api/chat"
            },
            "protected": {
                "update_profile": "PUT /api/profile (requires auth)",
                "crud_skills": "POST/PUT/DELETE /api/skills (requires auth)",
                "crud_projects": "POST/PUT/DELETE /api/projects (requires auth)"
            },
            "auth": {
                "login": "POST /api/auth/login",
                "verify": "GET /api/auth/verify",
                "status": "GET /api/auth/status"
            },
            "export": {
                "resume": "GET /api/export/resume?lang=ja&format=pdf",
                "preview": "GET /api/export/resume/preview?lang=ja"
            }
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "sqlite"}
