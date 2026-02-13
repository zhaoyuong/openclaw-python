"""Shell completion generation for OpenClaw CLI"""
from __future__ import annotations

import sys
from pathlib import Path


def generate_bash_completion() -> str:
    """Generate bash completion script"""
    return """# OpenClaw bash completion
_openclaw_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Top-level commands
    opts="start status health gateway agent config memory models skills tools channels browser system cron hooks plugins security sandbox nodes tui onboard setup doctor version help"
    
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}

complete -F _openclaw_completion openclaw
"""


def generate_zsh_completion() -> str:
    """Generate zsh completion script"""
    return """#compdef openclaw

_openclaw() {
    local -a commands
    commands=(
        'start:Start OpenClaw server'
        'status:Show system status'
        'health:Health check'
        'gateway:Gateway management'
        'agent:Agent operations'
        'config:Configuration management'
        'memory:Memory search'
        'models:Model configuration'
        'skills:Skills management'
        'tools:Tools management'
        'channels:Channel management'
        'browser:Browser automation'
        'system:System events'
        'cron:Cron scheduler'
        'hooks:Hooks management'
        'plugins:Plugin management'
        'security:Security management'
        'sandbox:Sandbox management'
        'nodes:Node management'
        'tui:Terminal UI'
        'onboard:Run onboarding wizard'
        'setup:Run setup wizard'
        'doctor:Run diagnostics'
        'version:Show version'
        'help:Show help'
    )
    
    _describe 'openclaw commands' commands
}

_openclaw
"""


def generate_fish_completion() -> str:
    """Generate fish completion script"""
    return """# OpenClaw fish completion

complete -c openclaw -f
complete -c openclaw -n "__fish_use_subcommand" -a "start" -d "Start OpenClaw server"
complete -c openclaw -n "__fish_use_subcommand" -a "status" -d "Show system status"
complete -c openclaw -n "__fish_use_subcommand" -a "health" -d "Health check"
complete -c openclaw -n "__fish_use_subcommand" -a "gateway" -d "Gateway management"
complete -c openclaw -n "__fish_use_subcommand" -a "agent" -d "Agent operations"
complete -c openclaw -n "__fish_use_subcommand" -a "config" -d "Configuration management"
complete -c openclaw -n "__fish_use_subcommand" -a "memory" -d "Memory search"
complete -c openclaw -n "__fish_use_subcommand" -a "models" -d "Model configuration"
complete -c openclaw -n "__fish_use_subcommand" -a "skills" -d "Skills management"
complete -c openclaw -n "__fish_use_subcommand" -a "tools" -d "Tools management"
complete -c openclaw -n "__fish_use_subcommand" -a "channels" -d "Channel management"
complete -c openclaw -n "__fish_use_subcommand" -a "tui" -d "Terminal UI"
complete -c openclaw -n "__fish_use_subcommand" -a "onboard" -d "Run onboarding wizard"
complete -c openclaw -n "__fish_use_subcommand" -a "setup" -d "Run setup wizard"
complete -c openclaw -n "__fish_use_subcommand" -a "doctor" -d "Run diagnostics"
complete -c openclaw -n "__fish_use_subcommand" -a "version" -d "Show version"
"""


def install_completion(shell: str = "bash") -> bool:
    """Install shell completion script
    
    Args:
        shell: Shell type (bash, zsh, fish)
        
    Returns:
        True if installed successfully
    """
    if shell == "bash":
        script = generate_bash_completion()
        install_path = Path.home() / ".bash_completion.d" / "openclaw"
        install_path.parent.mkdir(parents=True, exist_ok=True)
    
    elif shell == "zsh":
        script = generate_zsh_completion()
        install_path = Path.home() / ".zsh" / "completion" / "_openclaw"
        install_path.parent.mkdir(parents=True, exist_ok=True)
    
    elif shell == "fish":
        script = generate_fish_completion()
        install_path = Path.home() / ".config" / "fish" / "completions" / "openclaw.fish"
        install_path.parent.mkdir(parents=True, exist_ok=True)
    
    else:
        print(f"❌ Unsupported shell: {shell}")
        return False
    
    # Write completion script
    install_path.write_text(script)
    print(f"✅ Completion script installed: {install_path}")
    
    # Instructions
    if shell == "bash":
        print("\n📝 Add to ~/.bashrc:")
        print(f"   source {install_path}")
    elif shell == "zsh":
        print("\n📝 Add to ~/.zshrc:")
        print(f"   fpath=(~/.zsh/completion $fpath)")
        print("   autoload -Uz compinit && compinit")
    elif shell == "fish":
        print("\n📝 Restart fish or run:")
        print("   source ~/.config/fish/config.fish")
    
    return True


async def setup_completion(mode: str = "quickstart") -> dict:
    """Setup shell completion during onboarding"""
    print("\n" + "=" * 60)
    print("🐚 SHELL COMPLETION SETUP")
    print("=" * 60)
    
    if mode == "quickstart":
        print("\n⚡ QuickStart: Skipping shell completion")
        print("💡 Run 'openclaw completion install' later to enable tab completion")
        return {"installed": False, "skipped": True}
    
    # Detect shell
    shell = Path(os.environ.get("SHELL", "/bin/bash")).name
    
    print(f"\n🔍 Detected shell: {shell}")
    
    response = input(f"\n❓ Install shell completion for {shell}? [y/N]: ").strip().lower()
    if response not in ["y", "yes"]:
        print("⏭️  Skipping completion setup")
        return {"installed": False, "skipped": True}
    
    success = install_completion(shell)
    
    return {"installed": success, "shell": shell}


__all__ = ["generate_bash_completion", "generate_zsh_completion", "generate_fish_completion", "install_completion", "setup_completion"]
