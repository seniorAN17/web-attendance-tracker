"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

from config import settings
from database import init_db
from routes import router

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A RESTful API for managing class attendance with AI predictions",
    version="1.0.0",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routes
app.include_router(router, prefix="/api", tags=["attendance"])

# Serve static files (frontend)
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page."""
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "message": "Web Attendance Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Web Attendance Tracker"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
