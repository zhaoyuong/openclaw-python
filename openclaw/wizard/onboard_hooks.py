"""Hooks setup during onboarding - aligned with TypeScript onboard-hooks.ts"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


async def setup_hooks(workspace_dir: Optional[Path] = None, mode: str = "quickstart") -> dict:
    """Setup internal hooks during onboarding
    
    Args:
        workspace_dir: Workspace directory path
        mode: "quickstart" or "advanced"
        
    Returns:
        Dict with hooks setup info
    """
    print("\n" + "=" * 60)
    print("🪝 HOOKS SETUP")
    print("=" * 60)
    
    if mode == "quickstart":
        print("\n⚡ QuickStart mode: Using default hooks configuration")
        # Configure session memory hooks on /new
        hooks_config = {
            "session_memory": {
                "enabled": True,
                "trigger": "/new",
                "action": "save_context"
            }
        }
        print("✅ Default hooks configured")
        return {"configured": True, "hooks": hooks_config}
    
    # Advanced mode
    print("\n🔧 Advanced hooks configuration:")
    print("  1. Session memory hooks (save context on /new)")
    print("  2. Custom webhook endpoints")
    print("  3. Event listeners")
    
    response = input("\n❓ Configure hooks now? [Y/n]: ").strip().lower()
    if response in ["n", "no"]:
        print("⏭️  Skipping hooks setup")
        return {"configured": False, "skipped": True}
    
    # Session memory hooks
    print("\n📝 Session Memory Hooks:")
    print("  Save conversation context when starting new session")
    
    enable_memory = input("  Enable? [Y/n]: ").strip().lower()
    if enable_memory not in ["n", "no"]:
        hooks_config = {
            "session_memory": {
                "enabled": True,
                "trigger": "/new",
                "action": "save_context"
            }
        }
        print("  ✅ Session memory hooks enabled")
    else:
        hooks_config = {}
    
    # Custom hooks directory
    if workspace_dir:
        hooks_dir = workspace_dir / "hooks"
        if not hooks_dir.exists():
            create_dir = input(f"\n  Create hooks directory at {hooks_dir}? [y/N]: ").strip().lower()
            if create_dir in ["y", "yes"]:
                hooks_dir.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ Created {hooks_dir}")
    
    print("\n✅ Hooks configured successfully")
    return {"configured": True, "hooks": hooks_config}


__all__ = ["setup_hooks"]
