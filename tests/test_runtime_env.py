"""Unit tests for RuntimeEnv"""

import pytest
from pathlib import Path
from openclaw.runtime_env import RuntimeEnv, RuntimeEnvManager


class TestRuntimeEnv:
    """Test RuntimeEnv class"""
    
    def test_create_runtime_env(self):
        """Test creating RuntimeEnv"""
        env = RuntimeEnv(
            env_id="test",
            model="anthropic/claude-sonnet-4",
            workspace=Path("./test_workspace")
        )
        
        assert env.env_id == "test"
        assert env.model == "anthropic/claude-sonnet-4"
        assert env.workspace.name == "test_workspace"
    
    def test_lazy_initialization(self):
        """Test that components are lazily initialized"""
        env = RuntimeEnv(
            env_id="test",
            model="anthropic/claude-sonnet-4"
        )
        
        # Components should not be created yet
        assert env._agent_runtime is None
        assert env._session_manager is None
        
        # Access should trigger creation
        runtime = env.agent_runtime
        assert runtime is not None
        assert env._agent_runtime is not None
    
    def test_session_manager_property(self):
        """Test session manager property"""
        env = RuntimeEnv(
            env_id="test",
            model="anthropic/claude-sonnet-4"
        )
        
        session_mgr = env.session_manager
        assert session_mgr is not None
        
        # Should return same instance
        assert env.session_manager is session_mgr
    
    def test_to_dict(self):
        """Test serialization"""
        env = RuntimeEnv(
            env_id="test",
            model="anthropic/claude-sonnet-4",
            config={"temperature": 0.7}
        )
        
        d = env.to_dict()
        assert d["env_id"] == "test"
        assert d["model"] == "anthropic/claude-sonnet-4"
        assert d["config"]["temperature"] == 0.7


class TestRuntimeEnvManager:
    """Test RuntimeEnvManager"""
    
    def test_create_env(self):
        """Test creating environment"""
        manager = RuntimeEnvManager()
        
        env = manager.create_env(
            "prod",
            "anthropic/claude-opus-4"
        )
        
        assert env.env_id == "prod"
        assert "prod" in manager.list_envs()
    
    def test_default_env(self):
        """Test default environment"""
        manager = RuntimeEnvManager()
        
        prod = manager.create_env("prod", "model-1")
        dev = manager.create_env("dev", "model-2")
        
        # First created should be default
        assert manager.get_default_env() == prod
        
        # Change default
        manager.set_default("dev")
        assert manager.get_default_env() == dev
    
    def test_get_env(self):
        """Test getting environment"""
        manager = RuntimeEnvManager()
        
        manager.create_env("test", "model-1")
        
        env = manager.get_env("test")
        assert env is not None
        assert env.env_id == "test"
        
        # Non-existent
        assert manager.get_env("nonexistent") is None
    
    def test_remove_env(self):
        """Test removing environment"""
        manager = RuntimeEnvManager()
        
        manager.create_env("test", "model-1")
        assert "test" in manager.list_envs()
        
        result = manager.remove_env("test")
        assert result is True
        assert "test" not in manager.list_envs()
    
    def test_list_envs(self):
        """Test listing environments"""
        manager = RuntimeEnvManager()
        
        manager.create_env("env1", "model-1")
        manager.create_env("env2", "model-2")
        manager.create_env("env3", "model-3")
        
        envs = manager.list_envs()
        assert len(envs) == 3
        assert "env1" in envs
        assert "env2" in envs
        assert "env3" in envs
    
    def test_to_dict(self):
        """Test serialization"""
        manager = RuntimeEnvManager()
        
        manager.create_env("prod", "model-1")
        manager.create_env("dev", "model-2")
        
        d = manager.to_dict()
        assert d["total_envs"] == 2
        assert d["default_env"] == "prod"
        assert "prod" in d["envs"]
        assert "dev" in d["envs"]
