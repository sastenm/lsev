from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="LSEV App Backend")

@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return "<!DOCTYPE html><html><head><title>LSEV</title></head><body><h1>Hello, World!</h1></body></html>"

@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}