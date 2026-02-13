"""Unit tests for abort signal"""
import pytest

from openclaw.agents.abort import AbortController, AbortError, AbortSignal


class TestAbortSignal:
    """Test AbortSignal class"""
    
    def test_create_signal(self):
        """Test creating abort signal"""
        signal = AbortSignal()
        assert not signal.aborted
        assert signal.reason is None
    
    def test_abort_signal(self):
        """Test aborting signal"""
        signal = AbortSignal()
        signal.abort()
        
        assert signal.aborted
    
    def test_abort_with_reason(self):
        """Test aborting with reason"""
        reason = Exception("Test abort")
        signal = AbortSignal()
        signal.abort(reason)
        
        assert signal.aborted
        assert signal.reason == reason
    
    def test_throw_if_aborted(self):
        """Test throw if aborted"""
        signal = AbortSignal()
        signal.abort()
        
        with pytest.raises(AbortError):
            signal.throw_if_aborted()
    
    def test_throw_if_not_aborted(self):
        """Test throw if not aborted (should not raise)"""
        signal = AbortSignal()
        
        # Should not raise
        signal.throw_if_aborted()


class TestAbortController:
    """Test AbortController class"""
    
    def test_create_controller(self):
        """Test creating abort controller"""
        controller = AbortController()
        assert controller.signal is not None
        assert not controller.signal.aborted
    
    def test_abort_through_controller(self):
        """Test aborting through controller"""
        controller = AbortController()
        controller.abort()
        
        assert controller.signal.aborted
    
    def test_abort_with_reason_through_controller(self):
        """Test aborting with reason through controller"""
        reason = Exception("Test")
        controller = AbortController()
        controller.abort(reason)
        
        assert controller.signal.aborted
        assert controller.signal.reason == reason
    
    def test_signal_shared(self):
        """Test that signal is shared"""
        controller = AbortController()
        signal1 = controller.signal
        signal2 = controller.signal
        
        assert signal1 is signal2
        
        controller.abort()
        assert signal1.aborted
        assert signal2.aborted


class TestAbortError:
    """Test AbortError exception"""
    
    def test_create_error(self):
        """Test creating abort error"""
        error = AbortError("Test abort")
        assert str(error) == "Test abort"
    
    def test_raise_error(self):
        """Test raising abort error"""
        with pytest.raises(AbortError) as exc_info:
            raise AbortError("Operation aborted")
        
        assert "Operation aborted" in str(exc_info.value)


@pytest.mark.asyncio
class TestAbortInAsyncContext:
    """Test abort signal in async context"""
    
    async def test_abort_async_operation(self):
        """Test aborting async operation"""
        import asyncio
        
        controller = AbortController()
        
        async def long_operation():
            for i in range(10):
                controller.signal.throw_if_aborted()
                await asyncio.sleep(0.01)
            return "completed"
        
        # Start operation
        task = asyncio.create_task(long_operation())
        
        # Abort after a bit
        await asyncio.sleep(0.03)
        controller.abort()
        
        # Operation should be aborted
        with pytest.raises(AbortError):
            await task
    
    async def test_multiple_abort_checks(self):
        """Test multiple abort checks"""
        signal = AbortSignal()
        
        # First check - should pass
        signal.throw_if_aborted()
        
        # Abort
        signal.abort()
        
        # Second check - should fail
        with pytest.raises(AbortError):
            signal.throw_if_aborted()
        
        # Third check - should also fail
        with pytest.raises(AbortError):
            signal.throw_if_aborted()
