import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, SessionLocal, engine
from .routers import goods, references, admin
from .seed_catalog import seed_catalog

Base.metadata.create_all(bind=engine)

if os.getenv("SEED_SAMPLE_CATALOG", "").lower() in {"1", "true", "yes", "on"}:
    db = SessionLocal()
    try:
        seed_catalog(db)
    finally:
        db.close()

app = FastAPI(title="Goods Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(goods.router)
app.include_router(references.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok"}
