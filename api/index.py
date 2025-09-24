from fastapi import FastAPI
from mangum import Mangum
import os
from app.database import get_db
from app.models import *
from app.api.endpoints import *

app = FastAPI()

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Autosell.mx API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "{{ $now }}"}

# Vercel handler
handler = Mangum(app)
