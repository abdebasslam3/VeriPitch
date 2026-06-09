import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="VeriPitch API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to VeriPitch API"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

from core.api.endpoints import router as api_router
from core.api.webhooks import router as webhook_router
from core.auth.routes import router as auth_router

app.include_router(api_router)
app.include_router(webhook_router)
app.include_router(auth_router)

handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
