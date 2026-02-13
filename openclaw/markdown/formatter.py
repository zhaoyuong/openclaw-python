"""Markdown formatting for different channels

Converts Markdown to channel-specific formats.
Matches TypeScript src/telegram/format.ts and src/slack/format.ts
"""
import re
from typing import Literal
from html import escape
import logging

logger = logging.getLogger(__name__)

MarkdownTableMode = Literal["off", "html", "markdown", "bullets", "code"]


def markdown_to_telegram_html(markdown: str, table_mode: MarkdownTableMode = "html") -> str:
    """
    Convert Markdown to Telegram HTML
    
    Telegram supports: <b>, <i>, <s>, <code>, <pre>, <a>
    Matches TypeScript markdownToTelegramHtml()
    
    Args:
        markdown: Input Markdown text
        table_mode: How to handle tables
        
    Returns:
        Telegram-compatible HTML
    """
    # Process tables first based on mode
    if table_mode == "code":
        markdown = convert_tables_to_code(markdown)
    elif table_mode == "bullets":
        markdown = convert_tables_to_bullets(markdown)
    elif table_mode == "off":
        markdown = remove_tables(markdown)
    
    # Convert Markdown to HTML-like format
    text = markdown
    
    # Code blocks with language
    text = re.sub(
        r'```(\w+)?\n(.*?)\n```',
        lambda m: f'<pre><code class="{m.group(1) or ""}">{escape(m.group(2))}</code></pre>',
        text,
        flags=re.DOTALL
    )
    
    # Inline code
    text = re.sub(r'`([^`]+)`', lambda m: f'<code>{escape(m.group(1))}</code>', text)
    
    # Bold
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)
    
    # Italic
    text = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', text)
    text = re.sub(r'_([^_]+)_', r'<i>\1</i>', text)
    
    # Strikethrough
    text = re.sub(r'~~([^~]+)~~', r'<s>\1</s>', text)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Clean up any remaining markdown syntax
    text = sanitize_for_telegram(text)
    
    return text


def sanitize_for_telegram(html: str) -> str:
    """
    Keep only Telegram-supported tags
    
    Matches TypeScript _sanitize_for_telegram logic
    """
    # Telegram supported tags
    allowed_tags = ['b', 'i', 's', 'code', 'pre', 'a']
    
    # Remove unsupported HTML tags but keep content
    # This is a simple implementation; for production use BeautifulSoup
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'span', 'ul', 'ol', 'li']:
        html = re.sub(f'<{tag}[^>]*>', '', html)
        html = re.sub(f'</{tag}>', '\n', html)
    
    # Convert strong/em to b/i
    html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
    html = html.replace('<em>', '<i>').replace('</em>', '</i>')
    
    return html


def convert_tables_to_code(markdown: str) -> str:
    """
    Convert Markdown tables to code blocks
    
    Matches TypeScript _convert_tables_to_code
    """
    # Find markdown tables
    table_pattern = r'\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n)+'
    
    def replace_table(match):
        table = match.group(0)
        return f"```\n{table}\n```"
    
    return re.sub(table_pattern, replace_table, markdown)


def convert_tables_to_bullets(markdown: str) -> str:
    """
    Convert Markdown tables to bullet lists
    
    Matches TypeScript _convert_tables_to_bullets
    """
    table_pattern = r'\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n)+'
    
    def replace_table(match):
        table = match.group(0)
        lines = table.strip().split('\n')
        
        if len(lines) < 3:
            return table
        
        # Parse header
        headers = [cell.strip() for cell in lines[0].split('|')[1:-1]]
        
        # Parse rows (skip separator line)
        result = []
        for line in lines[2:]:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            row_text = ', '.join(f"{h}: {c}" for h, c in zip(headers, cells))
            result.append(f"• {row_text}")
        
        return '\n'.join(result)
    
    return re.sub(table_pattern, replace_table, markdown)


def remove_tables(markdown: str) -> str:
    """Remove Markdown tables entirely"""
    table_pattern = r'\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n)+'
    return re.sub(table_pattern, '', markdown)


def markdown_to_slack_mrkdwn(markdown: str, table_mode: MarkdownTableMode = "code") -> str:
    """
    Convert Markdown to Slack mrkdwn format
    
    Slack uses its own flavor of markdown.
    Matches TypeScript src/slack/format.ts
    """
    # Process tables
    if table_mode == "code":
        markdown = convert_tables_to_code(markdown)
    elif table_mode == "bullets":
        markdown = convert_tables_to_bullets(markdown)
    
    text = markdown
    
    # Bold: **text** -> *text*
    text = re.sub(r'\*\*([^\*]+)\*\*', r'*\1*', text)
    
    # Italic: *text* -> _text_
    text = re.sub(r'(?<!\*)\*([^\*]+)\*(?!\*)', r'_\1_', text)
    
    # Code: `code` -> `code` (same)
    # Code blocks remain the same
    
    # Links: [text](url) -> <url|text>
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<\2|\1>', text)
    
    # Preserve Slack mentions and channel links
    # <@user>, <#channel> should not be modified
    
    return text


def markdown_to_discord_markdown(markdown: str, table_mode: MarkdownTableMode = "markdown") -> str:
    """
    Convert Markdown to Discord markdown
    
    Discord supports standard markdown with some extensions.
    Matches TypeScript src/discord/format.ts
    """
    # Process tables
    if table_mode == "code":
        markdown = convert_tables_to_code(markdown)
    elif table_mode == "bullets":
        markdown = convert_tables_to_bullets(markdown)
    elif table_mode == "off":
        markdown = remove_tables(markdown)
    
    # Discord largely supports standard markdown
    # Main conversion: ensure code blocks use Discord syntax
    
    return markdown
