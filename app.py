        from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse

app = FastAPI(title="HOP Live Engine", version="1.0")

@app.get("/")
def root():
    return {"ok": True, "service": "HOP Live Engine"}

@app.get("/status")
def status():
    return {"ok": True, "status": "up"}

@app.get("/mcp")
def mcp_handshake(x_api_key: str | None = Header(None)):
    if x_api_key != "EMET-ROOT-777":
        return JSONResponse(status_code=401, content={"error": "unauthorized"})

    return {
        "protocol": "mcp",
        "version": "1.0",
        "server": "HOP Live Engine",
        "capabilities": {
            "context": True,
            "tools": False,
            "resources": True
        }
    }    "resources": True
        }
    }
