"""Telegram-specific onboarding plugin

Guides users through Telegram bot setup during onboarding.
"""
from typing import Optional


def validate_telegram_config(config: dict) -> tuple[bool, Optional[str]]:
    """
    Validate Telegram configuration
    
    Args:
        config: Telegram configuration dict
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not config:
        return False, "Telegram configuration is empty"
    
    if not config.get("bot_token"):
        return False, "bot_token is required"
    
    # Validate token format (should be like: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)
    token = config["bot_token"]
    if ":" not in token:
        return False, "Invalid bot_token format"
    
    return True, None


async def test_telegram_connection(bot_token: str) -> tuple[bool, Optional[str]]:
    """
    Test connection to Telegram API
    
    Args:
        bot_token: Telegram bot token
        
    Returns:
        Tuple of (is_connected, error_message)
    """
    try:
        import aiohttp
        
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("ok"):
                        bot_info = data.get("result", {})
                        username = bot_info.get("username", "unknown")
                        return True, f"Connected successfully as @{username}"
                    else:
                        return False, f"API error: {data.get('description', 'Unknown error')}"
                else:
                    return False, f"HTTP error: {response.status}"
    except ImportError:
        # aiohttp not available, skip actual test
        return True, "Connection test skipped (aiohttp not installed)"
    except Exception as e:
        return False, f"Connection test failed: {str(e)}"


def get_onboarding_steps() -> list[dict]:
    """
    Get Telegram onboarding steps
    
    Returns:
        List of onboarding step descriptions
    """
    return [
        {
            "step": 1,
            "title": "Create Telegram Bot",
            "description": "Open Telegram and search for @BotFather",
            "instructions": [
                "Send /newbot to @BotFather",
                "Follow the prompts to choose a name and username",
                "Copy the bot token provided by BotFather",
            ]
        },
        {
            "step": 2,
            "title": "Configure Bot Token",
            "description": "Enter your bot token in the configuration",
            "instructions": [
                "Paste the token you received from BotFather",
                "The token should look like: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
            ]
        },
        {
            "step": 3,
            "title": "Set DM Policy",
            "description": "Choose who can message your bot",
            "instructions": [
                "Open: Allow all users (public)",
                "Pairing: Require approval (recommended for personal use)",
                "Allowlist: Specific users only",
            ]
        },
        {
            "step": 4,
            "title": "Test Connection",
            "description": "Verify bot is accessible",
            "instructions": [
                "Search for your bot username in Telegram",
                "Send a test message",
                "You should receive a response",
            ]
        },
    ]


def get_setup_guide() -> str:
    """
    Get comprehensive setup guide
    
    Returns:
        Markdown-formatted setup guide
    """
    return """
# Telegram Bot Setup Guide

## Prerequisites
- A Telegram account
- Access to the Telegram app

## Step-by-Step Setup

### 1. Create Your Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat with BotFather
3. Send the command `/newbot`
4. Choose a name for your bot (can be anything)
5. Choose a username for your bot (must end in 'bot', e.g., `myawesomebot`)
6. BotFather will provide your bot token - **save this!**

### 2. Configure OpenClaw

Add your bot token to the configuration:

```toml
[channels.telegram]
enabled = true
bot_token = "YOUR_BOT_TOKEN_HERE"
dm_policy = "pairing"  # or "open" or "allowlist"
```

### 3. DM Policy Options

- **open**: Anyone can message your bot (good for public bots)
- **pairing**: Users must be approved first (recommended for personal use)
- **allowlist**: Only specific user IDs can message the bot

### 4. Test Your Bot

1. Search for your bot username in Telegram
2. Send `/start` to begin
3. Try sending a message - your bot should respond!

## Troubleshooting

### Bot doesn't respond
- Verify the bot token is correct
- Check that the OpenClaw Gateway is running
- Ensure Telegram channel is enabled in config

### Permission errors
- Check your DM policy settings
- If using allowlist, ensure your user ID is included
- If using pairing, approve your connection request

## Advanced Configuration

### Custom Commands
You can customize bot commands through BotFather:
1. Message @BotFather
2. Send `/setcommands`
3. Select your bot
4. Define your commands

### Privacy Settings
Configure privacy through BotFather:
1. `/setprivacy` - Control group message visibility
2. `/setjoingroups` - Allow/disallow adding bot to groups

## Security Notes

⚠️ **Keep your bot token secure!**
- Never commit it to public repositories
- Use environment variables or secure config files
- Rotate the token if it's ever exposed (via @BotFather)
"""
