"""Screenshot capture utilities for browser automation

This module provides utilities for capturing screenshots and visual elements
from browser pages using Chrome DevTools Protocol.
"""
from __future__ import annotations

import base64
import logging
from io import BytesIO
from pathlib import Path
from typing import Any, Literal

from .cdp_helpers import CDPHelper

logger = logging.getLogger(__name__)


class ScreenshotError(Exception):
    """Screenshot capture error"""
    pass


async def capture_screenshot(
    cdp: CDPHelper,
    format: Literal["png", "jpeg"] = "png",
    quality: int = 80,
    full_page: bool = False,
    clip: dict[str, float] | None = None,
) -> bytes:
    """
    Capture screenshot of current page
    
    Args:
        cdp: CDP helper instance
        format: Image format ("png" or "jpeg")
        quality: JPEG quality (1-100, only for jpeg format)
        full_page: Capture full page (requires scrolling)
        clip: Clip region {x, y, width, height, scale}
        
    Returns:
        Screenshot image bytes
        
    Raises:
        ScreenshotError: If capture fails
    """
    try:
        params: dict[str, Any] = {
            "format": format,
        }
        
        if format == "jpeg":
            params["quality"] = quality
        
        if clip:
            params["clip"] = clip
        
        if full_page:
            # Get page dimensions
            metrics = await cdp.execute_command("Page.getLayoutMetrics")
            content_size = metrics["contentSize"]
            
            params["clip"] = {
                "x": 0,
                "y": 0,
                "width": content_size["width"],
                "height": content_size["height"],
                "scale": 1
            }
        
        result = await cdp.execute_command("Page.captureScreenshot", params)
        
        # Decode base64 data
        image_data = base64.b64decode(result["data"])
        return image_data
        
    except Exception as e:
        logger.error(f"Screenshot capture failed: {e}")
        raise ScreenshotError(f"Capture failed: {e}")


async def save_screenshot(
    cdp: CDPHelper,
    path: Path | str,
    format: Literal["png", "jpeg"] = "png",
    quality: int = 80,
    full_page: bool = False,
) -> None:
    """
    Capture and save screenshot to file
    
    Args:
        cdp: CDP helper instance
        path: Output file path
        format: Image format ("png" or "jpeg")
        quality: JPEG quality (1-100)
        full_page: Capture full page
        
    Raises:
        ScreenshotError: If capture or save fails
    """
    image_data = await capture_screenshot(
        cdp,
        format=format,
        quality=quality,
        full_page=full_page
    )
    
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "wb") as f:
        f.write(image_data)
    
    logger.info(f"Screenshot saved to: {path}")


async def capture_element_screenshot(
    cdp: CDPHelper,
    node_id: int,
    format: Literal["png", "jpeg"] = "png",
    quality: int = 80,
) -> bytes:
    """
    Capture screenshot of specific element
    
    Args:
        cdp: CDP helper instance
        node_id: DOM node ID
        format: Image format ("png" or "jpeg")
        quality: JPEG quality (1-100)
        
    Returns:
        Screenshot image bytes
        
    Raises:
        ScreenshotError: If capture fails
    """
    try:
        # Get element bounding box
        box_model = await cdp.execute_command("DOM.getBoxModel", {
            "nodeId": node_id
        })
        
        # Get content quad (border box)
        quad = box_model["model"]["border"]
        
        # Calculate clip region
        xs = [quad[i] for i in range(0, len(quad), 2)]
        ys = [quad[i] for i in range(1, len(quad), 2)]
        
        clip = {
            "x": min(xs),
            "y": min(ys),
            "width": max(xs) - min(xs),
            "height": max(ys) - min(ys),
            "scale": 1
        }
        
        # Capture with clip
        return await capture_screenshot(
            cdp,
            format=format,
            quality=quality,
            clip=clip
        )
        
    except Exception as e:
        logger.error(f"Element screenshot failed: {e}")
        raise ScreenshotError(f"Element capture failed: {e}")


async def capture_viewport_screenshot(
    cdp: CDPHelper,
    format: Literal["png", "jpeg"] = "png",
    quality: int = 80,
) -> bytes:
    """
    Capture screenshot of visible viewport only
    
    Args:
        cdp: CDP helper instance
        format: Image format ("png" or "jpeg")
        quality: JPEG quality (1-100)
        
    Returns:
        Screenshot image bytes
    """
    return await capture_screenshot(
        cdp,
        format=format,
        quality=quality,
        full_page=False
    )


def screenshot_to_base64(image_data: bytes) -> str:
    """
    Convert screenshot bytes to base64 data URL
    
    Args:
        image_data: Image bytes
        
    Returns:
        Base64 data URL (data:image/png;base64,...)
    """
    b64 = base64.b64encode(image_data).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def screenshot_to_pil_image(image_data: bytes):
    """
    Convert screenshot bytes to PIL Image
    
    Args:
        image_data: Image bytes
        
    Returns:
        PIL Image object
        
    Raises:
        ImportError: If PIL not installed
    """
    try:
        from PIL import Image
        return Image.open(BytesIO(image_data))
    except ImportError:
        raise ImportError("PIL/Pillow not installed. Install with: pip install Pillow")


async def capture_pdf(
    cdp: CDPHelper,
    landscape: bool = False,
    display_header_footer: bool = False,
    print_background: bool = True,
    scale: float = 1.0,
    paper_width: float = 8.5,
    paper_height: float = 11.0,
    margin_top: float = 0,
    margin_bottom: float = 0,
    margin_left: float = 0,
    margin_right: float = 0,
) -> bytes:
    """
    Capture page as PDF
    
    Args:
        cdp: CDP helper instance
        landscape: Use landscape orientation
        display_header_footer: Display header/footer
        print_background: Print background graphics
        scale: Page scale (0.1 to 2.0)
        paper_width: Paper width in inches
        paper_height: Paper height in inches
        margin_top: Top margin in inches
        margin_bottom: Bottom margin in inches
        margin_left: Left margin in inches
        margin_right: Right margin in inches
        
    Returns:
        PDF document bytes
        
    Raises:
        ScreenshotError: If PDF capture fails
    """
    try:
        result = await cdp.execute_command("Page.printToPDF", {
            "landscape": landscape,
            "displayHeaderFooter": display_header_footer,
            "printBackground": print_background,
            "scale": scale,
            "paperWidth": paper_width,
            "paperHeight": paper_height,
            "marginTop": margin_top,
            "marginBottom": margin_bottom,
            "marginLeft": margin_left,
            "marginRight": margin_right,
        })
        
        # Decode base64 PDF data
        pdf_data = base64.b64decode(result["data"])
        return pdf_data
        
    except Exception as e:
        logger.error(f"PDF capture failed: {e}")
        raise ScreenshotError(f"PDF capture failed: {e}")


async def save_pdf(
    cdp: CDPHelper,
    path: Path | str,
    **kwargs
) -> None:
    """
    Capture and save page as PDF
    
    Args:
        cdp: CDP helper instance
        path: Output PDF file path
        **kwargs: Arguments for capture_pdf()
        
    Raises:
        ScreenshotError: If capture or save fails
    """
    pdf_data = await capture_pdf(cdp, **kwargs)
    
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "wb") as f:
        f.write(pdf_data)
    
    logger.info(f"PDF saved to: {path}")
