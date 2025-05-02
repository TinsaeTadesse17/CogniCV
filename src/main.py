from fastapi import FastAPI
from src.routers import cv

app = FastAPI(title="CVForge API")
app.include_router(cv.router)

@app.get("/")
def health():
    return {"status": "ok"}
