from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import cv

app = FastAPI(title="CVForge API")

# Allow CORS from the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv.router)

@app.get("/")
def health():
    return {"status": "ok"}
