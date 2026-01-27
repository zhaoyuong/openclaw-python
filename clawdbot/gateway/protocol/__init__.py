"""Gateway protocol schemas and types"""

from .frames import RequestFrame, ResponseFrame, EventFrame, ErrorShape

__all__ = ["RequestFrame", "ResponseFrame", "EventFrame", "ErrorShape"]
