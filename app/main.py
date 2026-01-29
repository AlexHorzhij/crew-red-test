from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.logging_config import logger
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import engine, Base
from app.projects.router import router as projects_router
from app.places.router import router as places_router

# 1. Rate Limiting setup (DDoS protection)
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title="Travel Planner API",
    description="API for managing travel projects and places",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Trusted Host Middleware (prevent Host Header attacks)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

# 3. CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    logger.error(f"Database error: {exc}")
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred. Transaction rolled back."},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )


Base.metadata.create_all(bind=engine)

app.include_router(projects_router)
app.include_router(places_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Travel Planner API"}
