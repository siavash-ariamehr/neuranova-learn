from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.routers import auth, lessons, progress, nft, analytics, collaboration, lesson_generation, translation

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="NeuraNova Learn API",
    description="Educational platform API with AR/VR, AI learning, and multilingual support",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(progress.router)
app.include_router(nft.router)
app.include_router(analytics.router)
app.include_router(collaboration.router)
app.include_router(lesson_generation.router)
app.include_router(translation.router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
