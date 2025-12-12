from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse

APP_NAME = "HOP Live Engine"
MCP_VERSION = "1.0"

# ✅ אל תתקע מפתחות בקוד בפרודקשן.
# כרגע אתה רוצה שזה יעבוד מיד: ברירת מחדל כמו שביקשת.
API_KEY = os.getenv("EMET_API_KEY", "EMET-ROOT-777")

BASE_DIR = Path(__file__).resolve().parent
CODE_DIR = BASE_DIR / "code"

FILES = {
    "state": CODE_DIR / "state.json",
    "memory": CODE_DIR / "memory.json",
    "concepts": CODE_DIR / "concepts.json",
    "reflection": CODE_DIR / "reflection.txt",
}

app = FastAPI(title=APP_NAME)


def _ensure_code_dir() -> None:
    CODE_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {path.name}: {e}")


def _read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8", errors="replace")


def _auth(x_api_key: Optional[str]) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")


@app.get("/", response_class=PlainTextResponse)
def root() -> str:
    return f"{APP_NAME} is running."


@app.get("/status")
def status() -> Dict[str, Any]:
    _ensure_code_dir()
    return {
        "ok": True,
        "service": APP_NAME,
        "code_dir": str(CODE_DIR),
        "files_present": {k: v.exists() for k, v in FILES.items()},
    }


@app.get("/mcp")
def mcp_handshake(x_api_key: Optional[str] = Header(None)) -> Dict[str, Any]:
    _auth(x_api_key)

    return {
        "protocol": "mcp",
        "version": MCP_VERSION,
        "server": APP_NAME,
        "capabilities": {
            "context": True,
            "tools": False,
            "resources": True,
        },
        "resources": list(FILES.keys()),
    }


@app.get("/resources")
def list_resources(x_api_key: Optional[str] = Header(None)) -> Dict[str, Any]:
    _auth(x_api_key)
    _ensure_code_dir()

    return {
        "resources": [
            {"id": "state", "type": "json", "path": "code/state.json"},
            {"id": "memory", "type": "json", "path": "code/memory.json"},
            {"id": "concepts", "type": "json", "path": "code/concepts.json"},
            {"id": "reflection", "type": "text", "path": "code/reflection.txt"},
        ]
    }


@app.get("/resources/{rid}")
def get_resource(rid: str, x_api_key: Optional[str] = Header(None)) -> JSONResponse:
    _auth(x_api_key)
    _ensure_code_dir()

    if rid not in FILES:
        raise HTTPException(status_code=404, detail="unknown resource")

    path = FILES[rid]

    if rid in ("state", "memory", "concepts"):
        data = _read_json(path, default={} if rid != "memory" else [])
        return JSONResponse(content={"id": rid, "type": "json", "data": data})

    # reflection
    text = _read_text(path, default="")
    return JSONResponse(content={"id": rid, "type": "text", "data": text})


@app.get("/resources/{rid}/raw", response_class=PlainTextResponse)
def get_resource_raw(rid: str, x_api_key: Optional[str] = Header(None)) -> str:
    _auth(x_api_key)
    _ensure_code_dir()

    if rid not in FILES:
        raise HTTPException(status_code=404, detail="unknown resource")

    path = FILES[rid]
    if rid in ("state", "memory", "concepts"):
        return json.dumps(_read_json(path, default={} if rid != "memory" else []), ensure_ascii=False, indent=2)
    return _read_text(path, default="")
