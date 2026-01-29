from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.exceptions import setup_exception_handlers
from app.core.database import engine, Base
from app.projects.router import router as projects_router
from app.places.router import router as places_router

from app.core.config import settings

limiter = Limiter(
    key_func=get_remote_address, default_limits=[settings.DEFAULT_RATE_LIMIT]
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

setup_exception_handlers(app)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(projects_router)
app.include_router(places_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Travel Planner API"}
