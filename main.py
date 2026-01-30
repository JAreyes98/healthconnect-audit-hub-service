import threading
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
import models
from database import engine
from services.rabbit_worker import start_audit_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    worker_thread = threading.Thread(target=start_audit_consumer, daemon=True)
    worker_thread.start()
    yield

app = FastAPI(
    title="HealthConnect Audit Hub Service",
    lifespan=lifespan
)

@app.get("/health")
def health():
    return {"status": "active", "service": "audit-hub"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)