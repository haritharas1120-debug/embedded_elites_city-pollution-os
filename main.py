from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from database.connection import engine, Base
import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    from database.seed import seed_data
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Seed data
    await seed_data()
    yield
    # Clean up on shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.auth import router as auth_router
from routes.data import router as data_router
from routes.ai import router as ai_router

app.include_router(auth_router)
app.include_router(data_router)
app.include_router(ai_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Chennai Air Pollution Monitoring API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
