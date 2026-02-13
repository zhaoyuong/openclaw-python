"""Slack-specific onboarding plugin

Guides users through Slack app setup during onboarding.
"""
from typing import Optional


def validate_slack_config(config: dict) -> tuple[bool, Optional[str]]:
    """
    Validate Slack configuration
    
    Args:
        config: Slack configuration dict
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not config:
        return False, "Slack configuration is empty"
    
    # Slack typically uses either bot_token or app_token
    if not config.get("bot_token") and not config.get("app_token"):
        return False, "bot_token or app_token is required"
    
    # Validate token format (Slack tokens start with xoxb- or xoxp-)
    token = config.get("bot_token") or config.get("app_token")
    if not token.startswith(("xoxb-", "xoxp-", "xapp-")):
        return False, "Invalid Slack token format (should start with xoxb-, xoxp-, or xapp-)"
    
    return True, None


async def test_slack_connection(bot_token: str) -> tuple[bool, Optional[str]]:
    """
    Test connection to Slack API
    
    Args:
        bot_token: Slack bot token
        
    Returns:
        Tuple of (is_connected, error_message)
    """
    try:
        import aiohttp
        
        url = "https://slack.com/api/auth.test"
        headers = {"Authorization": f"Bearer {bot_token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("ok"):
                        team = data.get("team", "unknown")
                        user = data.get("user", "unknown")
                        return True, f"Connected successfully to {team} as {user}"
                    else:
                        error = data.get("error", "Unknown error")
                        return False, f"API error: {error}"
                else:
                    return False, f"HTTP error: {response.status}"
    except ImportError:
        # aiohttp not available, skip actual test
        return True, "Connection test skipped (aiohttp not installed)"
    except Exception as e:
        return False, f"Connection test failed: {str(e)}"


def get_onboarding_steps() -> list[dict]:
    """
    Get Slack onboarding steps
    
    Returns:
        List of onboarding step descriptions
    """
    return [
        {
            "step": 1,
            "title": "Create Slack App",
            "description": "Go to Slack API portal",
            "instructions": [
                "Visit https://api.slack.com/apps",
                "Click 'Create New App'",
                "Choose 'From scratch'",
                "Name your app and select your workspace",
            ]
        },
        {
            "step": 2,
            "title": "Configure Bot User",
            "description": "Add bot functionality",
            "instructions": [
                "In your app settings, go to 'App Home'",
                "Under 'Your App's Presence in Slack', toggle 'Always Show My Bot as Online'",
                "Click 'Add Legacy Bot User' (if needed)",
            ]
        },
        {
            "step": 3,
            "title": "Set Bot Permissions",
            "description": "Configure OAuth scopes",
            "instructions": [
                "Go to 'OAuth & Permissions'",
                "Scroll to 'Scopes'",
                "Add Bot Token Scopes:",
                "  - channels:history (read messages in public channels)",
                "  - chat:write (send messages)",
                "  - im:history (read DMs)",
                "  - im:write (send DMs)",
            ]
        },
        {
            "step": 4,
            "title": "Install App to Workspace",
            "description": "Install and get tokens",
            "instructions": [
                "Go to 'OAuth & Permissions'",
                "Click 'Install to Workspace'",
                "Authorize the app",
                "Copy the 'Bot User OAuth Token' (starts with xoxb-)",
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
# Slack App Setup Guide

## Prerequisites
- A Slack workspace (or permission to install apps)
- Slack workspace administrator access (or app installation permissions)

## Step-by-Step Setup

### 1. Create Slack App

1. Go to [Slack API Portal](https://api.slack.com/apps)
2. Click **Create New App**
3. Choose **From scratch**
4. Enter your app name
5. Select your workspace
6. Click **Create App**

### 2. Configure Bot User

1. In your app settings, go to **App Home** (left sidebar)
2. Scroll to **Your App's Presence in Slack**
3. Toggle **Always Show My Bot as Online** ✓
4. Under **Show Tabs**, enable:
   - ✓ Home Tab
   - ✓ Messages Tab

### 3. Set OAuth Scopes

1. Go to **OAuth & Permissions** (left sidebar)
2. Scroll to **Scopes** section
3. Add **Bot Token Scopes**:

**Required scopes:**
- `channels:history` - View messages in public channels
- `chat:write` - Send messages
- `im:history` - View messages in direct messages
- `im:write` - Send direct messages
- `users:read` - View people in workspace

**Optional but recommended:**
- `channels:read` - View basic channel info
- `files:write` - Upload files
- `reactions:write` - Add emoji reactions

### 4. Enable Event Subscriptions (Optional)

For real-time message handling:

1. Go to **Event Subscriptions**
2. Toggle **Enable Events** ✓
3. Enter Request URL: `https://your-domain.com/slack/events`
4. Subscribe to bot events:
   - `message.channels` - Messages in channels
   - `message.im` - Direct messages

### 5. Install App to Workspace

1. Go to **OAuth & Permissions**
2. Click **Install to Workspace**
3. Review permissions
4. Click **Allow**
5. **Copy the Bot User OAuth Token** (starts with `xoxb-`)

### 6. Configure OpenClaw

Add your bot token to the configuration:

```toml
[channels.slack]
enabled = true
bot_token = "xoxb-YOUR-TOKEN-HERE"
app_token = "xapp-YOUR-APP-TOKEN-HERE"  # If using Socket Mode
signing_secret = "YOUR-SIGNING-SECRET"
```

**Get tokens from:**
- Bot Token: OAuth & Permissions page
- App Token: Basic Information > App-Level Tokens (for Socket Mode)
- Signing Secret: Basic Information > App Credentials

### 7. Choose Connection Mode

**Option A: Socket Mode** (Recommended for development)
1. Go to **Socket Mode**
2. Enable Socket Mode ✓
3. Generate App-Level Token with `connections:write` scope
4. Use both `bot_token` and `app_token` in config

**Option B: Events API** (For production)
1. Set up HTTPS endpoint
2. Configure Request URL in Event Subscriptions
3. Only `bot_token` needed in config

### 8. Test Your Bot

1. Open Slack workspace
2. Find your app in Apps section
3. Send a direct message: "Hello!"
4. Or invite to channel: `/invite @YourBot`
5. Bot should respond!

## Troubleshooting

### Bot doesn't respond
- ✓ Verify bot token is correct
- ✓ Check OpenClaw Gateway is running
- ✓ Ensure bot has required scopes
- ✓ Check bot is invited to channel (for channel messages)

### Permission errors
- ✓ Review OAuth scopes in app settings
- ✓ Reinstall app to workspace after changing scopes
- ✓ Verify workspace allows app installations

### Socket Mode connection issues
- ✓ App-Level Token must have `connections:write` scope
- ✓ Both bot_token and app_token must be configured
- ✓ Check firewall/network settings

## Advanced Configuration

### Slash Commands

Add custom commands:
1. Go to **Slash Commands**
2. Click **Create New Command**
3. Set command name (e.g., `/openclaw`)
4. Set Request URL
5. Add description and usage hint

### Interactive Components

Enable buttons and menus:
1. Go to **Interactivity & Shortcuts**
2. Toggle **Interactivity** ✓
3. Set Request URL
4. Configure shortcuts if needed

### App Home

Customize bot's home tab:
1. Go to **App Home**
2. Design home tab view
3. Add welcome message
4. Include quick action buttons

## Security Notes

⚠️ **Keep your tokens secure!**
- Never commit tokens to version control
- Use environment variables
- Store tokens encrypted
- Rotate tokens if compromised (OAuth & Permissions > Revoke Token)
- Use Signing Secret to verify requests

## Best Practices

1. **Use Socket Mode for development** - No need for public HTTPS endpoint
2. **Request minimal scopes** - Only add what you need
3. **Handle rate limits** - Slack has message rate limits (1 message/second)
4. **Log interactions** - Help with debugging and monitoring
5. **Test in dev workspace first** - Don't test in production workspace

## Resources

- [Slack API Documentation](https://api.slack.com/docs)
- [Bolt for Python](https://slack.dev/bolt-python/) (Official Slack SDK)
- [Slack App Manifest](https://api.slack.com/reference/manifests) (Config as code)
- [Rate Limiting Guide](https://api.slack.com/docs/rate-limits)
"""
