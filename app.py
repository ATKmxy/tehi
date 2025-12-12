# app.py
from __future__ import annotations

import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="tehi / HOP MCP Gateway", version="1.0")

API_KEY = os.getenv("HOP_API_KEY", "EMET-ROOT-777")

@app.get("/status")
def status():
    return {"ok": True, "service": "tehi", "api_key_required": bool(API_KEY)}

@app.get("/mcp")
def mcp_handshake(x_api_key: str | None = Header(None)):
    # allow either header style: x-api-key OR Authorization: Bearer <key>
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")

    return {
        "protocol": "mcp",
        "version": "1.0",
        "server": "HOP Live Engine",
        "capabilities": {"context": True, "tools": False, "resources": True},
    }
