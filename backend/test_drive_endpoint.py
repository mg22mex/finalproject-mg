#!/usr/bin/env python3
"""
Test Drive endpoint directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.api.drive import router as drive_router

app = FastAPI()
app.include_router(drive_router, prefix="/drive", tags=["drive"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
