from fastapi import FastAPI
from .database import Base, engine
from .routers import orders, admin_orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", version="1.0.0")

app.include_router(orders.router)
app.include_router(admin_orders.router)


@app.get("/health")
def health():
    return {"status": "ok"}