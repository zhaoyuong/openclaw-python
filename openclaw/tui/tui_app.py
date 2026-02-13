"""OpenClaw Terminal User Interface - aligned with TypeScript pi-tui implementation"""
from __future__ import annotations

import asyncio
import logging
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer, Vertical
from textual.widgets import Footer, Header, Input, Static
from textual.reactive import reactive

from openclaw.config.loader import load_config

logger = logging.getLogger(__name__)


class ChatMessage(Static):
    """A single chat message widget"""
    
    def __init__(self, role: str, content: str, **kwargs):
        super().__init__(**kwargs)
        self.role = role
        self.content = content
    
    def render(self) -> str:
        """Render the message"""
        if self.role == "user":
            return f"[bold cyan]You:[/bold cyan] {self.content}"
        elif self.role == "assistant":
            return f"[bold green]Assistant:[/bold green] {self.content}"
        else:
            return f"[dim]{self.content}[/dim]"


class ChatLog(ScrollableContainer):
    """Chat message history container"""
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat log"""
        message = ChatMessage(role, content)
        self.mount(message)
        self.scroll_end()


class StatusBar(Static):
    """Status bar showing connection and model info"""
    
    connection_status = reactive("disconnected")
    current_model = reactive("unknown")
    token_count = reactive(0)
    
    def render(self) -> str:
        """Render status bar"""
        status_indicator = "🟢" if self.connection_status == "connected" else "🔴"
        return f"{status_indicator} {self.connection_status} | Model: {self.current_model} | Tokens: {self.token_count}"


class OpenClawTUI(App):
    """OpenClaw Terminal User Interface Application"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #chat_log {
        height: 1fr;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }
    
    #status_bar {
        height: 1;
        background: $boost;
        color: $text;
        padding: 0 1;
    }
    
    #input_area {
        height: 3;
        margin: 0 1 1 1;
    }
    
    ChatMessage {
        margin: 0 0 1 0;
    }
    """
    
    TITLE = "OpenClaw AI Assistant"
    SUB_TITLE = "Powered by Claude/Gemini/GPT"
    
    BINDINGS = [
        Binding("ctrl+c", "clear_or_quit", "Clear/Quit", show=True),
        Binding("ctrl+d", "quit", "Quit", show=True),
        Binding("ctrl+g", "agent_selector", "Agent", show=False),
        Binding("ctrl+l", "model_selector", "Model", show=False),
        Binding("ctrl+p", "session_selector", "Session", show=False),
        Binding("ctrl+n", "new_session", "New", show=True),
        Binding("escape", "abort_run", "Abort", show=False),
    ]
    
    def __init__(self, gateway_url: Optional[str] = None, gateway_token: Optional[str] = None):
        super().__init__()
        self.gateway_url = gateway_url or "ws://localhost:18789"
        self.gateway_token = gateway_token
        self.ws_connection = None
        self.chat_log: Optional[ChatLog] = None
        self.status_bar: Optional[StatusBar] = None
        self.input_widget: Optional[Input] = None
    
    def compose(self) -> ComposeResult:
        """Create TUI layout"""
        yield Header()
        
        # Chat log
        self.chat_log = ChatLog(id="chat_log")
        yield self.chat_log
        
        # Status bar
        self.status_bar = StatusBar(id="status_bar")
        yield self.status_bar
        
        # Input area
        yield Container(
            Input(
                placeholder="Type a message and press Enter...",
                id="input_area"
            ),
            id="input_container"
        )
        
        yield Footer()
    
    async def on_mount(self) -> None:
        """Called when app starts"""
        # Get input widget
        self.input_widget = self.query_one("#input_area", Input)
        self.input_widget.focus()
        
        # Connect to Gateway
        await self.connect_gateway()
        
        # Welcome message
        if self.chat_log:
            self.chat_log.add_message("system", "Welcome to OpenClaw TUI! Type /help for commands.")
    
    async def connect_gateway(self) -> None:
        """Connect to Gateway WebSocket"""
        try:
            # TODO: Implement WebSocket connection
            if self.status_bar:
                self.status_bar.connection_status = "connecting"
            
            # For now, simulate connection
            await asyncio.sleep(0.5)
            
            if self.status_bar:
                self.status_bar.connection_status = "connected"
                self.status_bar.current_model = "claude-sonnet-4"
            
            logger.info(f"Connected to gateway: {self.gateway_url}")
        except Exception as e:
            logger.error(f"Failed to connect to gateway: {e}")
            if self.status_bar:
                self.status_bar.connection_status = "error"
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission"""
        message = event.value.strip()
        if not message:
            return
        
        # Clear input
        self.input_widget.value = ""
        
        # Add user message to chat
        if self.chat_log:
            self.chat_log.add_message("user", message)
        
        # Handle slash commands
        if message.startswith("/"):
            await self.handle_slash_command(message)
        else:
            # Send to agent
            await self.send_to_agent(message)
    
    async def handle_slash_command(self, command: str) -> None:
        """Handle TUI slash commands"""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == "/help":
            help_text = """
Available Commands:
  /help - Show this help
  /new - Start new session
  /status - Show status
  /model - Show/set model
  /exit - Exit TUI
            """
            if self.chat_log:
                self.chat_log.add_message("system", help_text.strip())
        
        elif cmd == "/exit" or cmd == "/quit":
            self.exit()
        
        elif cmd == "/new":
            if self.chat_log:
                self.chat_log.add_message("system", "✨ New session started")
        
        elif cmd == "/status":
            status = f"""
Status:
  Connection: {self.status_bar.connection_status if self.status_bar else 'unknown'}
  Model: {self.status_bar.current_model if self.status_bar else 'unknown'}
  Tokens: {self.status_bar.token_count if self.status_bar else 0}
            """
            if self.chat_log:
                self.chat_log.add_message("system", status.strip())
        
        else:
            if self.chat_log:
                self.chat_log.add_message("system", f"Unknown command: {cmd}")
    
    async def send_to_agent(self, message: str) -> None:
        """Send message to agent via Gateway"""
        # Show typing indicator
        if self.chat_log:
            typing_msg = ChatMessage("system", "💭 Thinking...")
            self.chat_log.mount(typing_msg)
        
        try:
            # TODO: Send via WebSocket to Gateway
            # For now, mock response
            await asyncio.sleep(1)
            
            # Remove typing indicator
            if typing_msg:
                typing_msg.remove()
            
            # Add assistant response
            response = "I received your message! (Gateway integration pending)"
            if self.chat_log:
                self.chat_log.add_message("assistant", response)
        
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            if self.chat_log:
                self.chat_log.add_message("system", f"❌ Error: {str(e)}")
    
    def action_clear_or_quit(self) -> None:
        """Clear input or quit on double Ctrl+C"""
        if self.input_widget and self.input_widget.value:
            self.input_widget.value = ""
        else:
            self.exit()
    
    def action_new_session(self) -> None:
        """Start new session"""
        if self.chat_log:
            self.chat_log.add_message("system", "✨ New session started")
    
    def action_model_selector(self) -> None:
        """Open model selector"""
        if self.chat_log:
            self.chat_log.add_message("system", "Model selector (Ctrl+L) - TODO: implement overlay")
    
    def action_agent_selector(self) -> None:
        """Open agent selector"""
        if self.chat_log:
            self.chat_log.add_message("system", "Agent selector (Ctrl+G) - TODO: implement overlay")
    
    def action_session_selector(self) -> None:
        """Open session selector"""
        if self.chat_log:
            self.chat_log.add_message("system", "Session selector (Ctrl+P) - TODO: implement overlay")
    
    def action_abort_run(self) -> None:
        """Abort current run"""
        if self.chat_log:
            self.chat_log.add_message("system", "⏹️ Run aborted")


async def run_tui(
    gateway_url: Optional[str] = None,
    gateway_token: Optional[str] = None
) -> None:
    """Run the TUI application"""
    app = OpenClawTUI(gateway_url=gateway_url, gateway_token=gateway_token)
    await app.run_async()


__all__ = ["OpenClawTUI", "run_tui"]
