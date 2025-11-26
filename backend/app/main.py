from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import questions, stats
from app.database import engine
from app.database import Base

# Create FastAPI app
app = FastAPI(
    title="Interview Prep API",
    description="API for interview preparation questions with AI-powered features",
    version="1.0.0"
)

# CORS middleware (allows frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(questions.router, prefix="/api", tags=["Questions"])
app.include_router(stats.router, prefix="/api", tags=["Statistics"])

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Interview Prep API",
        "docs": "/docs",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}