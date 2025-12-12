from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse

app = FastAPI(title="tehi / HOP MCP Server")

API_KEY = "EMET-ROOT-777"


@app.get("/")
def root():
    return {
        "service": "tehi",
        "status": "alive",
        "protocol": "http"
    }


@app.get("/status")
def status():
    return {
        "ok": True,
        "service": "tehi",
        "runtime": "fastapi"
    }


@app.get("/mcp")
def mcp_handshake(x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized"}
        )

    return {
        "protocol": "mcp",
        "version": "1.0",
        "server": "HOP Live Engine",
        "capabilities": {
            "context": True,
            "tools": False,
            "resources": True
        }
    }
