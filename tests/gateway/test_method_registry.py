"""Unit tests for Gateway Method Registry"""

import pytest
from openclaw.gateway.api import MethodRegistry, get_method_registry
from openclaw.gateway.api.methods import ConnectMethod, PingMethod, AgentMethod


class TestMethodRegistry:
    """Test MethodRegistry"""
    
    def test_create_registry(self):
        """Test creating registry"""
        registry = MethodRegistry()
        assert registry.get_method_count() == 0
    
    def test_register_method(self):
        """Test registering methods"""
        registry = MethodRegistry()
        
        registry.register(ConnectMethod())
        assert registry.has("connect")
        assert registry.get_method_count() == 1
    
    def test_get_method(self):
        """Test getting method"""
        registry = MethodRegistry()
        connect = ConnectMethod()
        registry.register(connect)
        
        method = registry.get("connect")
        assert method is not None
        assert method.name == "connect"
    
    def test_unregister_method(self):
        """Test unregistering method"""
        registry = MethodRegistry()
        registry.register(ConnectMethod())
        
        assert registry.has("connect")
        result = registry.unregister("connect")
        assert result is True
        assert not registry.has("connect")
    
    def test_list_all(self):
        """Test listing all methods"""
        registry = MethodRegistry()
        registry.register(ConnectMethod())
        registry.register(PingMethod())
        registry.register(AgentMethod())
        
        methods = registry.list_all()
        assert len(methods) == 3
        assert "connect" in methods
        assert "ping" in methods
        assert "agent" in methods
    
    def test_list_by_category(self):
        """Test listing by category"""
        registry = MethodRegistry()
        registry.register(ConnectMethod())  # connection
        registry.register(PingMethod())     # connection
        registry.register(AgentMethod())    # agent
        
        connection_methods = registry.list_by_category("connection")
        assert len(connection_methods) == 2
        assert "connect" in connection_methods
        assert "ping" in connection_methods
        
        agent_methods = registry.list_by_category("agent")
        assert len(agent_methods) == 1
        assert "agent" in agent_methods
    
    def test_get_categories(self):
        """Test getting all categories"""
        registry = MethodRegistry()
        registry.register(ConnectMethod())
        registry.register(AgentMethod())
        
        categories = registry.get_categories()
        assert "connection" in categories
        assert "agent" in categories
    
    def test_generate_docs(self):
        """Test API documentation generation"""
        registry = MethodRegistry()
        registry.register(ConnectMethod())
        registry.register(AgentMethod())
        
        docs = registry.generate_docs()
        
        assert docs["total_methods"] == 2
        assert "connection" in docs["categories"]
        assert "agent" in docs["categories"]
        assert "connect" in docs["methods"]
        assert "agent" in docs["methods"]
        
        connect_doc = docs["methods"]["connect"]
        assert connect_doc["name"] == "connect"
        assert connect_doc["category"] == "connection"
        assert connect_doc["description"]
    
    def test_to_dict(self):
        """Test registry serialization"""
        registry = MethodRegistry()
        registry.register(ConnectMethod())
        registry.register(PingMethod())
        
        d = registry.to_dict()
        assert d["total_methods"] == 2
        assert "connection" in d["categories"]
        assert "connect" in d["methods"]


class TestMethods:
    """Test individual methods"""
    
    @pytest.mark.asyncio
    async def test_connect_method(self):
        """Test ConnectMethod execution"""
        method = ConnectMethod()
        
        class MockConnection:
            client_info = None
            protocol_version = 0
            authenticated = False
        
        conn = MockConnection()
        
        result = await method.execute(conn, {
            "maxProtocol": 1,
            "client": {
                "name": "test",
                "version": "1.0",
                "platform": "test"
            }
        })
        
        assert result["protocol"] == 1
        assert result["server"]["name"] == "openclaw-python"
        assert conn.authenticated is True
    
    @pytest.mark.asyncio
    async def test_ping_method(self):
        """Test PingMethod execution"""
        method = PingMethod()
        
        class MockConnection:
            pass
        
        result = await method.execute(MockConnection(), {"timestamp": 123})
        assert result["pong"] is True
        assert result["timestamp"] == 123
    
    @pytest.mark.asyncio
    async def test_health_method(self):
        """Test HealthMethod execution"""
        from openclaw.gateway.api.methods import HealthMethod
        
        method = HealthMethod()
        
        class MockConnection:
            gateway = None
        
        result = await method.execute(MockConnection(), {})
        assert "status" in result
        assert result["status"] == "healthy"


def test_global_registry():
    """Test global registry"""
    registry = get_method_registry()
    
    # Should have core methods registered
    assert registry.get_method_count() >= 5
    assert registry.has("connect")
    assert registry.has("ping")
    assert registry.has("health")
    assert registry.has("agent")
