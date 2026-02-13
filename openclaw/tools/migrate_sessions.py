"""
Session storage migration tool

Migrate from old per-session JSON files to centralized sessions.json format.
"""

import json
import logging
import time
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import uuid

from openclaw.agents.session_entry import SessionEntry
from openclaw.config.sessions.store import save_session_store
from openclaw.config.sessions.transcripts import write_transcript_line

logger = logging.getLogger(__name__)


# ============================================================================
# Migration Functions
# ============================================================================

def migrate_to_centralized_store(
    workspace_dir: Path,
    agent_id: str = "main",
    backup: bool = True,
    dry_run: bool = False
) -> Dict[str, any]:
    """
    Migrate from per-session JSON files to centralized sessions.json
    
    Args:
        workspace_dir: Workspace directory containing .sessions/
        agent_id: Agent identifier (default: "main")
        backup: Whether to backup old files (default: True)
        dry_run: If True, only analyze without making changes
        
    Returns:
        Dict with migration statistics
    """
    sessions_dir = workspace_dir / ".sessions"
    
    if not sessions_dir.exists():
        logger.warning(f"Sessions directory not found: {sessions_dir}")
        return {
            "status": "not_found",
            "sessions_found": 0,
            "migrated": 0,
            "errors": 0,
        }
    
    # Find all session JSON files (exclude session_map.json)
    session_files = [
        f for f in sessions_dir.glob("*.json")
        if f.name != "session_map.json" and f.name != "sessions.json"
    ]
    
    logger.info(f"Found {len(session_files)} session files to migrate")
    
    if dry_run:
        logger.info("DRY RUN MODE - no changes will be made")
    
    # Statistics
    stats = {
        "status": "success",
        "sessions_found": len(session_files),
        "migrated": 0,
        "errors": 0,
        "error_details": [],
    }
    
    # Build centralized store
    centralized_store: Dict[str, SessionEntry] = {}
    
    # Process each session file
    for session_file in session_files:
        session_id = session_file.stem
        
        try:
            # Load old session data
            with open(session_file, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            
            # Extract messages
            messages = old_data.get("messages", [])
            metadata = old_data.get("metadata", {})
            created_at = old_data.get("created_at")
            updated_at = old_data.get("updated_at")
            
            # Convert timestamps
            created_at_ms = _parse_timestamp_to_ms(created_at)
            updated_at_ms = _parse_timestamp_to_ms(updated_at)
            
            # Create SessionEntry
            # Build a key for this session
            # Try to derive from metadata or use sessionId
            session_key = metadata.get("session_key", f"agent:{agent_id}:{session_id[:8]}")
            
            entry = SessionEntry(
                session_id=session_id,
                updated_at=updated_at_ms,
                session_file=f"{session_id}.jsonl",
                # Preserve metadata if available
                label=metadata.get("label"),
                display_name=metadata.get("display_name"),
            )
            
            centralized_store[session_key] = entry
            
            # Create transcript file from messages
            if not dry_run and messages:
                transcript_path = sessions_dir / f"{session_id}.jsonl"
                _write_messages_to_transcript(messages, transcript_path)
            
            stats["migrated"] += 1
            logger.info(f"Migrated session: {session_key} ({session_id})")
            
        except Exception as e:
            logger.error(f"Failed to migrate {session_file}: {e}")
            stats["errors"] += 1
            stats["error_details"].append({
                "file": str(session_file),
                "error": str(e)
            })
    
    # Save centralized store
    if not dry_run and centralized_store:
        store_path = sessions_dir / "sessions.json"
        save_session_store(str(store_path), centralized_store)
        logger.info(f"Saved centralized store to {store_path}")
    
    # Backup old files
    if backup and not dry_run and stats["migrated"] > 0:
        backup_dir = sessions_dir / "backup_old_format"
        backup_dir.mkdir(exist_ok=True)
        
        for session_file in session_files:
            backup_path = backup_dir / session_file.name
            shutil.copy2(session_file, backup_path)
        
        # Also backup session_map.json if exists
        session_map = sessions_dir / "session_map.json"
        if session_map.exists():
            shutil.copy2(session_map, backup_dir / "session_map.json")
        
        logger.info(f"Backed up {len(session_files)} files to {backup_dir}")
        stats["backup_dir"] = str(backup_dir)
    
    return stats


def _parse_timestamp_to_ms(timestamp_str: Optional[str]) -> int:
    """Parse ISO timestamp string to milliseconds since epoch"""
    if not timestamp_str:
        return int(time.time() * 1000)
    
    try:
        from datetime import datetime
        
        # Try parsing ISO format
        dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)
    except Exception:
        # Fallback to current time
        return int(time.time() * 1000)


def _write_messages_to_transcript(messages: List[dict], transcript_path: Path) -> None:
    """Write messages to transcript file in JSONL format"""
    with open(transcript_path, 'w', encoding='utf-8') as f:
        for msg in messages:
            # Convert to JSONL format
            line = {
                "role": msg.get("role", "user"),
                "content": msg.get("content", ""),
                "timestamp": msg.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
            }
            
            # Include optional fields
            if "tool_calls" in msg:
                line["tool_calls"] = msg["tool_calls"]
            if "tool_call_id" in msg:
                line["tool_call_id"] = msg["tool_call_id"]
            if "name" in msg:
                line["name"] = msg["name"]
            if "images" in msg:
                line["images"] = msg["images"]
            
            json.dump(line, f, ensure_ascii=False)
            f.write('\n')


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for migration tool"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migrate session storage from per-file to centralized format"
    )
    parser.add_argument(
        "workspace_dir",
        type=Path,
        help="Workspace directory containing .sessions/"
    )
    parser.add_argument(
        "--agent-id",
        default="main",
        help="Agent identifier (default: main)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip backing up old files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze without making changes"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run migration
    logger.info(f"Starting migration for workspace: {args.workspace_dir}")
    
    stats = migrate_to_centralized_store(
        workspace_dir=args.workspace_dir,
        agent_id=args.agent_id,
        backup=not args.no_backup,
        dry_run=args.dry_run
    )
    
    # Print results
    print("\n" + "="*60)
    print("Migration Results")
    print("="*60)
    print(f"Status: {stats['status']}")
    print(f"Sessions found: {stats['sessions_found']}")
    print(f"Sessions migrated: {stats['migrated']}")
    print(f"Errors: {stats['errors']}")
    
    if stats.get("backup_dir"):
        print(f"Backup location: {stats['backup_dir']}")
    
    if stats["errors"] > 0:
        print("\nErrors:")
        for error in stats["error_details"]:
            print(f"  {error['file']}: {error['error']}")
    
    print("="*60)
    
    if args.dry_run:
        print("\nDRY RUN - No changes were made")
    else:
        print("\nMigration complete!")
    
    return 0 if stats["errors"] == 0 else 1


if __name__ == "__main__":
    exit(main())
