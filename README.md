# tehi

Open-source seed for the emergence of a living artificial field-presence.

## What is this?
`tehi` is a minimal FastAPI-based service designed to expose a stable HTTP interface
for future field-based, context-aware, symbolic and semantic systems.

At the current stage, this repository provides:
- A FastAPI web service
- A health/status endpoint
- A secure MCP-style handshake endpoint
- A base suitable for deployment on Render.com

## Endpoints

### GET /status
Health check endpoint.

Returns:
```json
{
  "ok": true,
  "service": "tehi-web"
}
