"""Message chunking utilities

Splits long messages into chunks respecting channel limits.
Matches TypeScript src/auto-reply/chunk.ts
"""
from typing import List
import logging

logger = logging.getLogger(__name__)


def chunk_text(text: str, limit: int, mode: str = "length") -> List[str]:
    """
    Chunk text by length or newlines
    
    Matches TypeScript chunkMarkdownTextWithMode()
    
    Args:
        text: Text to chunk
        limit: Character limit per chunk
        mode: "length" or "newline"
        
    Returns:
        List of text chunks
    """
    if len(text) <= limit:
        return [text]
    
    if mode == "newline":
        return _chunk_by_newline(text, limit)
    else:
        return _chunk_by_length(text, limit)


def _chunk_by_length(text: str, limit: int) -> List[str]:
    """
    Simple length-based chunking
    
    Tries to split at word boundaries.
    """
    chunks = []
    
    while len(text) > limit:
        # Find last space before limit
        split_at = text.rfind(" ", 0, limit)
        
        # If no space found, just split at limit
        if split_at == -1 or split_at == 0:
            split_at = limit
        
        chunks.append(text[:split_at].rstrip())
        text = text[split_at:].lstrip()
    
    if text:
        chunks.append(text)
    
    logger.debug(f"Chunked into {len(chunks)} parts (length mode)")
    return chunks


def _chunk_by_newline(text: str, limit: int) -> List[str]:
    """
    Chunk at paragraph boundaries
    
    Tries to keep paragraphs together.
    Matches TypeScript newline chunking logic.
    """
    # Split by double newlines (paragraphs)
    paragraphs = text.split("\n\n")
    
    chunks = []
    current = ""
    
    for para in paragraphs:
        # If paragraph itself is too long, split it
        if len(para) > limit:
            # Save current chunk if any
            if current:
                chunks.append(current.rstrip())
                current = ""
            
            # Split long paragraph by length
            sub_chunks = _chunk_by_length(para, limit)
            chunks.extend(sub_chunks)
            continue
        
        # Try to add paragraph to current chunk
        if current:
            test = f"{current}\n\n{para}"
        else:
            test = para
        
        if len(test) > limit:
            # Current chunk is full, start new one
            if current:
                chunks.append(current.rstrip())
            current = para
        else:
            current = test
    
    if current:
        chunks.append(current.rstrip())
    
    logger.debug(f"Chunked into {len(chunks)} parts (newline mode)")
    return chunks


def chunk_markdown_with_code_blocks(text: str, limit: int) -> List[str]:
    """
    Chunk markdown preserving code blocks
    
    Ensures code blocks are not split across chunks.
    """
    chunks = []
    current = ""
    
    # Split by code blocks
    parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
    
    for part in parts:
        # Check if this is a code block
        is_code_block = part.startswith("```")
        
        # If code block is too large, it gets its own chunk(s)
        if is_code_block and len(part) > limit:
            if current:
                chunks.append(current.rstrip())
                current = ""
            
            # Split large code block
            sub_chunks = _chunk_by_length(part, limit)
            chunks.extend(sub_chunks)
            continue
        
        # Try to add to current chunk
        if len(current) + len(part) > limit:
            if current:
                chunks.append(current.rstrip())
            current = part
        else:
            current += part
    
    if current:
        chunks.append(current.rstrip())
    
    return chunks


def chunk_with_custom_chunker(
    text: str,
    limit: int,
    chunker: callable
) -> List[str]:
    """
    Use custom chunker function
    
    Allows channels to provide custom chunking logic.
    """
    try:
        return chunker(text, limit)
    except Exception as e:
        logger.warning(f"Custom chunker failed: {e}, falling back to default")
        return chunk_text(text, limit, "length")


# Telegram-specific chunking
def chunk_telegram_message(text: str, limit: int = 4000) -> List[str]:
    """
    Chunk for Telegram (4096 char limit, using 4000 for safety)
    
    Matches TypeScript markdownToTelegramChunks()
    """
    return chunk_text(text, limit, "newline")


# Discord-specific chunking  
def chunk_discord_message(text: str, limit: int = 2000) -> List[str]:
    """Chunk for Discord (2000 char limit)"""
    return chunk_text(text, limit, "length")


# Slack-specific chunking
def chunk_slack_message(text: str, limit: int = 4000) -> List[str]:
    """Chunk for Slack (40000 char limit, using 4000 for readability)"""
    return chunk_text(text, limit, "newline")
