"""Control UI static file serving

Serves the Control UI web interface.
Matches TypeScript control UI integration.
"""
import logging
from pathlib import Path
from aiohttp import web

logger = logging.getLogger(__name__)


async def serve_control_ui(app: web.Application):
    """
    Serve Control UI static files
    
    Provides the web management interface for OpenClaw.
    """
    # Get UI directory path
    ui_dir = Path(__file__).parent.parent.parent / "ui" / "dist"
    
    if not ui_dir.exists():
        logger.warning(f"Control UI not found at {ui_dir}")
        logger.warning("Run 'cd ui && pnpm install && pnpm build' to build UI")
        return
    
    # Check if index.html exists
    index_file = ui_dir / "index.html"
    if not index_file.exists():
        logger.warning(f"Control UI index.html not found at {index_file}")
        return
    
    # Serve index.html at root
    async def index_handler(request):
        """Serve index.html"""
        return web.FileResponse(index_file)
    
    # Serve static assets
    assets_dir = ui_dir / "assets"
    if assets_dir.exists():
        app.router.add_static("/assets", assets_dir, name="ui_assets")
    
    # Favicon
    favicon = ui_dir.parent.parent / "public" / "favicon.svg"
    if not favicon.exists():
        favicon = ui_dir / "favicon.svg"
    
    if favicon.exists():
        async def favicon_handler(request):
            return web.FileResponse(favicon)
        app.router.add_get("/favicon.svg", favicon_handler)
    
    # Register index handler
    app.router.add_get("/", index_handler)
    app.router.add_get("/index.html", index_handler)
    
    # Handle SPA routing - serve index.html for all non-API routes
    async def spa_handler(request):
        """Serve index.html for SPA routes"""
        path = request.path
        # Don't intercept API, WebSocket, or asset requests
        if path.startswith(("/ws", "/api", "/assets", "/favicon")):
            raise web.HTTPNotFound()
        return web.FileResponse(index_file)
    
    # This should be last to catch all other routes
    app.router.add_get("/{tail:.*}", spa_handler)
    
    logger.info(f"✅ Control UI served from {ui_dir}")
    logger.info("Access UI at: http://localhost:18789/")
