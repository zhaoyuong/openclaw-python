"""
Tests for memory manager

Matches TypeScript memory tests
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from openclaw.memory.manager import SimpleMemorySearchManager, get_memory_search_manager
from openclaw.memory.types import MemorySource


class TestMemoryManager:
    """Tests for memory search manager."""

    @pytest.mark.asyncio
    async def test_create_manager(self):
        """Test creating a memory manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            manager = await get_memory_search_manager(workspace)

            assert manager is not None
            status = manager.status()
            assert status.backend == "builtin"

    @pytest.mark.asyncio
    async def test_search_empty_workspace(self):
        """Test searching empty workspace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            manager = await get_memory_search_manager(workspace)

            results = await manager.search("test query")
            assert results == []

    @pytest.mark.asyncio
    async def test_search_memory_file(self):
        """Test searching MEMORY.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            # Create MEMORY.md
            memory_file = workspace / "MEMORY.md"
            memory_file.write_text("""# Project Memory

## Tasks
- Implement feature X
- Fix bug Y

## Decisions
- Use Python for backend
""")

            manager = await get_memory_search_manager(workspace)

            results = await manager.search("Python")

            assert len(results) > 0
            assert any("Python" in r.snippet for r in results)
            assert all(r.source == MemorySource.MEMORY for r in results)

    @pytest.mark.asyncio
    async def test_search_memory_directory(self):
        """Test searching memory/*.md files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            # Create memory directory
            memory_dir = workspace / "memory"
            memory_dir.mkdir()

            # Create memory files
            (memory_dir / "project.md").write_text("Project documentation")
            (memory_dir / "notes.md").write_text("Important notes")

            manager = await get_memory_search_manager(workspace)

            results = await manager.search("documentation")

            assert len(results) > 0
            assert any("documentation" in r.snippet for r in results)

    @pytest.mark.asyncio
    async def test_read_file(self):
        """Test reading file from memory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            memory_file = workspace / "MEMORY.md"
            memory_file.write_text("""Line 1
Line 2
Line 3
Line 4
Line 5
""")

            manager = await get_memory_search_manager(workspace)

            # Read full file
            result = await manager.read_file({"relPath": "MEMORY.md"})
            assert "Line 1" in result["text"]
            assert "Line 5" in result["text"]

            # Read specific lines
            result = await manager.read_file({"relPath": "MEMORY.md", "from": 2, "lines": 2})
            text = result["text"]
            assert "Line 2" in text
            assert "Line 3" in text
            assert "Line 1" not in text
            assert "Line 4" not in text


class TestMemoryProviderStatus:
    """Tests for memory provider status."""

    @pytest.mark.asyncio
    async def test_status(self):
        """Test getting provider status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            # Create some memory files
            (workspace / "MEMORY.md").write_text("Memory content")
            memory_dir = workspace / "memory"
            memory_dir.mkdir()
            (memory_dir / "notes.md").write_text("Notes")

            manager = await get_memory_search_manager(workspace)
            status = manager.status()

            assert status.backend == "builtin"
            assert status.provider == "simple-text-search"
            assert status.files == 2
            assert workspace.name in str(status.workspace_dir)
