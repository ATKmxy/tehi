import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

APP_NAME = "HOP Live Engine"
API_KEY = os.getenv("HOP_API_KEY", "EMET-ROOT-777")

app = FastAPI(title=APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def require_key(x_api_key: str | None):
    if not API_KEY:
        return
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")

@app.get("/status")
def status():
    return {"ok": True, "service": APP_NAME}

@app.get("/mcp")
def mcp_handshake(x_api_key: str | None = Header(None)):
    require_key(x_api_key)
    return {
        "protocol": "mcp",
        "version": "1.0",
        "server": APP_NAME,
        "capabilities": {
            "context": True,
            "tools": False,
            "resources": True
        }
    }
