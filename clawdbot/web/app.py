"""Web UI FastAPI application"""

import logging
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..config import load_config
from ..agents.session import SessionManager
from ..channels.registry import get_channel_registry

logger = logging.getLogger(__name__)

app = FastAPI(title="ClawdBot Control Panel")

# Setup templates and static files
templates_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"

templates = Jinja2Templates(directory=str(templates_dir))

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Control panel home page"""
    config = load_config()
    channel_registry = get_channel_registry()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "config": config,
        "channels": channel_registry.list_channels()
    })


@app.get("/webchat", response_class=HTMLResponse)
async def webchat(request: Request):
    """WebChat interface"""
    return templates.TemplateResponse("webchat.html", {
        "request": request
    })


@app.get("/api/status")
async def api_status():
    """Get system status"""
    config = load_config()
    channel_registry = get_channel_registry()

    return {
        "status": "ok",
        "gateway": {
            "port": config.gateway.port,
            "bind": config.gateway.bind
        },
        "channels": [
            {
                "id": ch.id,
                "label": ch.label,
                "running": ch.is_running()
            }
            for ch in channel_registry.list_channels()
        ]
    }


@app.get("/api/sessions")
async def api_sessions():
    """List sessions"""
    session_manager = SessionManager()
    session_ids = session_manager.list_sessions()

    return {
        "sessions": [
            {"id": sid, "messageCount": 0}  # TODO: Get actual message count
            for sid in session_ids
        ]
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            # Handle different message types
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif data.get("type") == "chat":
                # TODO: Handle chat message
                await websocket.send_json({
                    "type": "chat_response",
                    "text": "Echo: " + data.get("text", "")
                })

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)


def create_web_app() -> FastAPI:
    """Create and configure the web application"""
    return app
