"""Discord-specific onboarding plugin

Guides users through Discord bot setup during onboarding.
"""
from typing import Optional


def validate_discord_config(config: dict) -> tuple[bool, Optional[str]]:
    """
    Validate Discord configuration
    
    Args:
        config: Discord configuration dict
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not config:
        return False, "Discord configuration is empty"
    
    if not config.get("bot_token"):
        return False, "bot_token is required"
    
    # Discord tokens are typically longer and have a specific format
    token = config["bot_token"]
    if len(token) < 50:
        return False, "Discord bot token appears too short"
    
    return True, None


async def test_discord_connection(bot_token: str) -> tuple[bool, Optional[str]]:
    """
    Test connection to Discord API
    
    Args:
        bot_token: Discord bot token
        
    Returns:
        Tuple of (is_connected, error_message)
    """
    try:
        import aiohttp
        
        url = "https://discord.com/api/v10/users/@me"
        headers = {"Authorization": f"Bot {bot_token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    username = data.get("username", "unknown")
                    return True, f"Connected successfully as {username}"
                elif response.status == 401:
                    return False, "Invalid bot token"
                else:
                    return False, f"HTTP error: {response.status}"
    except ImportError:
        # aiohttp not available, skip actual test
        return True, "Connection test skipped (aiohttp not installed)"
    except Exception as e:
        return False, f"Connection test failed: {str(e)}"


def get_onboarding_steps() -> list[dict]:
    """
    Get Discord onboarding steps
    
    Returns:
        List of onboarding step descriptions
    """
    return [
        {
            "step": 1,
            "title": "Create Discord Application",
            "description": "Go to Discord Developer Portal",
            "instructions": [
                "Visit https://discord.com/developers/applications",
                "Click 'New Application' and give it a name",
                "Go to the 'Bot' section in the left sidebar",
                "Click 'Add Bot' and confirm",
            ]
        },
        {
            "step": 2,
            "title": "Get Bot Token",
            "description": "Copy your bot token",
            "instructions": [
                "In the Bot section, click 'Reset Token'",
                "Copy the token that appears",
                "This token will only be shown once!",
            ]
        },
        {
            "step": 3,
            "title": "Configure Bot Permissions",
            "description": "Set required permissions",
            "instructions": [
                "Scroll to 'Privileged Gateway Intents'",
                "Enable 'MESSAGE CONTENT INTENT' (required for reading messages)",
                "Enable 'SERVER MEMBERS INTENT' (if needed)",
                "Save changes",
            ]
        },
        {
            "step": 4,
            "title": "Invite Bot to Server",
            "description": "Add bot to your Discord server",
            "instructions": [
                "Go to OAuth2 > URL Generator",
                "Select scope: 'bot'",
                "Select permissions: 'Send Messages', 'Read Messages/View Channels'",
                "Copy the generated URL and open it",
                "Select your server and authorize",
            ]
        },
    ]


def get_setup_guide() -> str:
    """
    Get comprehensive setup guide
    
    Returns:
        Markdown-formatted setup guide
    """
    return """# Discord Bot Setup Guide

## Prerequisites
- A Discord account
- Administrator access to a Discord server (or create your own)

## Quick Setup Steps

1. Go to Discord Developer Portal
2. Create New Application
3. Add Bot and copy token
4. Enable MESSAGE CONTENT INTENT
5. Generate invite URL and add to server

## Detailed Instructions

Visit the full guide for step-by-step instructions on creating
and configuring your Discord bot for OpenClaw.
"""
