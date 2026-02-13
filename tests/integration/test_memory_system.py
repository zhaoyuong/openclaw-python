"""Integration tests for memory system"""
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from openclaw.memory.builtin_manager import BuiltinMemoryManager


@pytest.mark.asyncio
class TestMemorySystem:
    """Test memory system integration"""
    
    async def test_create_memory_manager(self):
        """Test creating memory manager"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(storage_path=Path(tmpdir))
            assert manager is not None
    
    async def test_add_and_search_memory(self):
        """Test adding and searching memory"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(storage_path=Path(tmpdir))
            
            # Add memory
            memory_id = await manager.add(
                content="Python is a programming language",
                tags=["programming", "python"]
            )
            
            assert memory_id is not None
            
            # Search memory
            results = await manager.search("programming language")
            
            assert len(results) > 0
            assert any("Python" in r.get("content", "") for r in results)
    
    async def test_hybrid_search(self):
        """Test hybrid search"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(storage_path=Path(tmpdir))
            
            # Add multiple memories
            await manager.add("Python is great for data science")
            await manager.add("JavaScript runs in browsers")
            await manager.add("Python has excellent libraries")
            
            # Search with hybrid mode
            results = await manager.search(
                query="Python",
                search_type="hybrid",
                limit=10
            )
            
            assert len(results) > 0
    
    async def test_memory_with_embeddings(self):
        """Test memory with embeddings"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(
                storage_path=Path(tmpdir),
                use_embeddings=True
            )
            
            # Add memory
            await manager.add("Machine learning is a subset of AI")
            
            # Semantic search
            results = await manager.search(
                query="artificial intelligence",
                search_type="semantic"
            )
            
            # Should find related content even with different wording
            assert isinstance(results, list)
    
    async def test_memory_tags(self):
        """Test memory tagging"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(storage_path=Path(tmpdir))
            
            # Add with tags
            await manager.add(
                content="React is a UI library",
                tags=["react", "frontend", "javascript"]
            )
            
            # Search by tag
            results = await manager.search_by_tag("frontend")
            
            assert len(results) > 0
    
    async def test_delete_memory(self):
        """Test deleting memory"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(storage_path=Path(tmpdir))
            
            # Add memory
            memory_id = await manager.add("Temporary content")
            
            # Delete
            deleted = await manager.delete(memory_id)
            assert deleted
            
            # Verify deleted
            result = await manager.get(memory_id)
            assert result is None


@pytest.mark.asyncio
class TestMemoryPersistence:
    """Test memory persistence"""
    
    async def test_memory_persists_across_restarts(self):
        """Test that memory persists"""
        with TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir)
            
            # First manager instance
            manager1 = BuiltinMemoryManager(storage_path=storage_path)
            memory_id = await manager1.add("Persistent content")
            
            # Create new manager instance (simulating restart)
            manager2 = BuiltinMemoryManager(storage_path=storage_path)
            await manager2.load()
            
            # Should find the memory
            result = await manager2.get(memory_id)
            assert result is not None
            assert "Persistent content" in result.get("content", "")
    
    async def test_memory_export(self):
        """Test exporting memory"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(storage_path=Path(tmpdir))
            
            # Add some memories
            await manager.add("Memory 1")
            await manager.add("Memory 2")
            
            # Export
            export_path = Path(tmpdir) / "export.json"
            await manager.export(export_path)
            
            assert export_path.exists()
    
    async def test_memory_import(self):
        """Test importing memory"""
        with TemporaryDirectory() as tmpdir:
            manager = BuiltinMemoryManager(storage_path=Path(tmpdir))
            
            # Create export
            export_path = Path(tmpdir) / "import.json"
            export_data = [
                {"content": "Imported memory 1", "tags": ["test"]},
                {"content": "Imported memory 2", "tags": ["test"]},
            ]
            
            import json
            with open(export_path, "w") as f:
                json.dump(export_data, f)
            
            # Import
            imported = await manager.import_from(export_path)
            
            assert imported > 0
            
            # Verify imported
            results = await manager.search_by_tag("test")
            assert len(results) >= 2


def test_memory_system_imports():
    """Test that memory system can be imported"""
    try:
        from openclaw.memory import BuiltinMemoryManager
        from openclaw.memory.embeddings import EmbeddingProvider
        from openclaw.memory.hybrid import HybridSearch
        
        assert BuiltinMemoryManager is not None
        assert EmbeddingProvider is not None
        assert HybridSearch is not None
    except ImportError as e:
        pytest.fail(f"Failed to import memory modules: {e}")
