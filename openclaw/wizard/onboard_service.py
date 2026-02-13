"""System service installation - aligned with TypeScript onboarding.finalize.ts"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def detect_runtime() -> str:
    """Detect Python runtime (python, uv, poetry)"""
    # Check if running with uv
    if "UV_PROJECT_ENVIRONMENT" in os.environ:
        return "uv"
    
    # Check if in poetry environment
    if "POETRY_ACTIVE" in os.environ:
        return "poetry"
    
    # Default to python
    return "python"


async def install_systemd_service(runtime: str = "python") -> bool:
    """Install OpenClaw as systemd user service (Linux)"""
    print("\n📦 Installing systemd service...")
    
    # Create service file
    service_content = f"""[Unit]
Description=OpenClaw AI Gateway
After=network.target

[Service]
Type=simple
ExecStart={sys.executable} -m openclaw gateway run
Restart=always
RestartSec=10
Environment="PATH={os.environ.get('PATH', '')}"
WorkingDirectory={Path.cwd()}

[Install]
WantedBy=default.target
"""
    
    # Service file path
    service_file = Path.home() / ".config" / "systemd" / "user" / "openclaw.service"
    service_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write service file
    service_file.write_text(service_content)
    print(f"  ✅ Service file created: {service_file}")
    
    # Enable and start service
    try:
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "--user", "enable", "openclaw"], check=True)
        subprocess.run(["systemctl", "--user", "start", "openclaw"], check=True)
        print("  ✅ Service installed and started")
        
        # Enable lingering (allows service to run when not logged in)
        subprocess.run(["loginctl", "enable-linger", os.getlogin()], check=False)
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install service: {e}")
        return False


async def install_launchd_service(runtime: str = "python") -> bool:
    """Install OpenClaw as launchd service (macOS)"""
    print("\n📦 Installing launchd service...")
    
    # Create plist
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>-m</string>
        <string>openclaw</string>
        <string>gateway</string>
        <string>run</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>{Path.cwd()}</string>
    <key>StandardOutPath</key>
    <string>{Path.home()}/Library/Logs/openclaw.log</string>
    <key>StandardErrorPath</key>
    <string>{Path.home()}/Library/Logs/openclaw.error.log</string>
</dict>
</plist>
"""
    
    # Plist file path
    plist_file = Path.home() / "Library" / "LaunchAgents" / "com.openclaw.gateway.plist"
    plist_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write plist
    plist_file.write_text(plist_content)
    print(f"  ✅ Service file created: {plist_file}")
    
    # Load service
    try:
        subprocess.run(["launchctl", "load", str(plist_file)], check=True)
        print("  ✅ Service loaded and started")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to load service: {e}")
        return False


async def install_windows_service(runtime: str = "python") -> bool:
    """Install OpenClaw as Windows Service"""
    print("\n📦 Installing Windows service...")
    print("  ℹ️  Windows service installation requires admin privileges")
    print("  ℹ️  Consider using Task Scheduler or NSSM instead")
    
    # TODO: Implement Windows service installation
    print("  ⚠️  Windows service installation not yet implemented")
    print("  💡 Alternative: Use Task Scheduler to run at startup:")
    print(f"     Program: {sys.executable}")
    print("     Arguments: -m openclaw gateway run")
    
    return False


async def install_service(mode: str = "quickstart") -> dict:
    """Install OpenClaw as system service
    
    Args:
        mode: "quickstart" or "advanced"
        
    Returns:
        Dict with installation result
    """
    print("\n" + "=" * 60)
    print("🚀 SYSTEM SERVICE INSTALLATION")
    print("=" * 60)
    
    if mode == "quickstart":
        prompt = "\n❓ Install OpenClaw as system service? [Y/n]: "
    else:
        prompt = "\n❓ Install OpenClaw as system service? [y/N]: "
    
    response = input(prompt).strip().lower()
    
    if mode == "quickstart":
        should_install = response not in ["n", "no"]
    else:
        should_install = response in ["y", "yes"]
    
    if not should_install:
        print("⏭️  Skipping service installation")
        return {"installed": False, "skipped": True}
    
    # Detect runtime
    runtime = detect_runtime()
    print(f"\n🔧 Detected runtime: {runtime}")
    
    # Platform-specific installation
    if sys.platform == "linux":
        success = await install_systemd_service(runtime)
    elif sys.platform == "darwin":
        success = await install_launchd_service(runtime)
    elif sys.platform == "win32":
        success = await install_windows_service(runtime)
    else:
        print(f"  ⚠️  Unsupported platform: {sys.platform}")
        success = False
    
    if success:
        print("\n✅ Service installed successfully")
        print("💡 Gateway will now start automatically on system boot")
        
        # Show service commands
        if sys.platform == "linux":
            print("\n📋 Service commands:")
            print("  systemctl --user status openclaw")
            print("  systemctl --user stop openclaw")
            print("  systemctl --user restart openclaw")
            print("  journalctl --user -u openclaw -f")
        elif sys.platform == "darwin":
            print("\n📋 Service commands:")
            print("  launchctl list | grep openclaw")
            print("  launchctl stop com.openclaw.gateway")
            print("  launchctl unload ~/Library/LaunchAgents/com.openclaw.gateway.plist")
    
    return {
        "installed": success,
        "platform": sys.platform,
        "runtime": runtime
    }


__all__ = ["install_service", "setup_skills", "detect_package_manager", "list_available_skills"]
