from fastapi import FastAPI
from .database import Base, engine
from .routers import goods, references, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Goods Service", version="1.0.0")

app.include_router(goods.router)
app.include_router(references.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok"}