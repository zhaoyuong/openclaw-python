"""End-to-end tests for onboarding flow

Tests the complete onboarding experience from first-run detection
to configuration completion and marker file creation.
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from openclaw.wizard.onboarding import (
    run_onboarding_wizard,
    is_first_run,
    mark_onboarding_complete,
    _confirm_risks,
    _select_mode,
)


class TestFirstRunDetection:
    """Test first-run detection"""
    
    def test_is_first_run_new_workspace(self):
        """Test that new workspace is detected as first run"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            assert is_first_run(workspace) is True
    
    def test_is_first_run_with_marker(self):
        """Test that workspace with marker is not first run"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            # Create marker file
            mark_onboarding_complete(workspace)
            assert is_first_run(workspace) is False
    
    def test_marker_file_creation(self):
        """Test onboarding marker file is created correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            mark_onboarding_complete(workspace)
            
            marker_file = workspace / ".openclaw" / "onboarding-complete"
            assert marker_file.exists()
            
            # Check marker file content
            import json
            content = json.loads(marker_file.read_text())
            assert "completed_at" in content
            assert "version" in content
            assert content["version"] == "0.6.0"


class TestOnboardingWizardQuickStart:
    """Test QuickStart onboarding mode"""
    
    @pytest.mark.asyncio
    async def test_quickstart_mode_basic(self):
        """Test basic QuickStart onboarding flow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            # Mock user inputs
            inputs = [
                "y",  # Confirm risks
                "1",  # QuickStart mode
                "1",  # Anthropic provider
                "test-api-key",  # API key
                "Y",  # Save configuration
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.wizard.auth.save_auth_to_env"):
                    with patch("openclaw.config.loader.save_config"):
                        result = await run_onboarding_wizard(
                            config=None,
                            workspace_dir=workspace
                        )
            
            assert result["completed"] is True
            assert result.get("mode") == "quickstart"
            assert result.get("provider") == "anthropic"
    
    @pytest.mark.asyncio
    async def test_quickstart_with_env_api_key(self):
        """Test QuickStart with existing environment API key"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            inputs = [
                "y",  # Confirm risks
                "1",  # QuickStart mode
                "Y",  # Use env API key
                "Y",  # Save configuration
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.wizard.auth.check_env_api_key", return_value="env-key"):
                    with patch("openclaw.config.loader.save_config"):
                        result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is True


class TestOnboardingWizardAdvanced:
    """Test Advanced onboarding mode"""
    
    @pytest.mark.asyncio
    async def test_advanced_mode_full_config(self):
        """Test Advanced mode with full configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            inputs = [
                "y",  # Confirm risks
                "2",  # Advanced mode
                "3",  # Reset config
                "2",  # OpenAI provider
                "test-openai-key",  # API key
                "2",  # Medium think level
                "",  # Default workspace
                "9000",  # Custom port
                "1",  # Loopback bind
                "1",  # Token auth
                "n",  # Skip channels
                "Y",  # Save configuration
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.wizard.auth.save_auth_to_env"):
                    with patch("openclaw.config.loader.save_config"):
                        result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is True
            assert result.get("mode") == "advanced"


class TestOnboardingRejection:
    """Test onboarding rejection scenarios"""
    
    @pytest.mark.asyncio
    async def test_risk_rejection(self):
        """Test onboarding when user rejects risks"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            inputs = ["n"]  # Reject risks
            
            with patch("builtins.input", side_effect=inputs):
                result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is False
            assert result["skipped"] is True
            assert "declined" in result.get("reason", "").lower()
    
    @pytest.mark.asyncio
    async def test_save_rejection(self):
        """Test onboarding when user rejects saving config"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            inputs = [
                "y",  # Confirm risks
                "1",  # QuickStart
                "1",  # Anthropic
                "test-key",  # API key
                "n",  # Don't save
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.wizard.auth.save_auth_to_env"):
                    result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is False
            assert result["skipped"] is True


class TestOnboardingConfigPersistence:
    """Test configuration persistence"""
    
    @pytest.mark.asyncio
    async def test_config_saved_correctly(self):
        """Test that configuration is saved correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            saved_config = None
            
            def mock_save_config(config):
                nonlocal saved_config
                saved_config = config
            
            inputs = [
                "y",  # Confirm risks
                "1",  # QuickStart
                "1",  # Anthropic
                "test-key",
                "Y",  # Save
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.wizard.auth.save_auth_to_env"):
                    with patch("openclaw.config.loader.save_config", side_effect=mock_save_config):
                        result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is True
            assert saved_config is not None


class TestOnboardingExistingConfig:
    """Test onboarding with existing configuration"""
    
    @pytest.mark.asyncio
    async def test_keep_existing_config(self):
        """Test keeping existing configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            # Mock existing config
            from openclaw.config.schema import ClawdbotConfig
            existing_config = ClawdbotConfig()
            
            inputs = [
                "y",  # Confirm risks
                "2",  # Advanced mode
                "1",  # Keep existing
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.config.loader.load_config", return_value=existing_config):
                    result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is True
            assert result.get("kept_existing") is True
    
    @pytest.mark.asyncio
    async def test_modify_existing_config(self):
        """Test modifying existing configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            from openclaw.config.schema import ClawdbotConfig
            existing_config = ClawdbotConfig()
            
            inputs = [
                "y",  # Confirm risks
                "2",  # Advanced mode
                "2",  # Modify
                "1",  # Anthropic
                "new-key",
                "",  # Default think level
                "",  # Default workspace
                "",  # Default port
                "",  # Default bind
                "",  # Default auth
                "n",  # Skip channels
                "Y",  # Save
            ]
            
            with patch("builtins.input", side_effect=inputs):
                with patch("openclaw.config.loader.load_config", return_value=existing_config):
                    with patch("openclaw.wizard.auth.save_auth_to_env"):
                        with patch("openclaw.config.loader.save_config"):
                            result = await run_onboarding_wizard(workspace_dir=workspace)
            
            assert result["completed"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
