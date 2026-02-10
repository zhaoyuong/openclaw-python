"""Command argument parsing

Parses command arguments according to command definitions.
Matches TypeScript src/auto-reply/commands-registry.ts
"""
import re
from typing import Dict, Any, List, Optional


def parse_command_args(command_def: dict, args_text: str) -> Dict[str, Any]:
    """
    Parse command arguments according to definition
    
    Matches TypeScript parseCommandArgs() logic
    
    Args:
        command_def: Command definition with args specification
        args_text: Raw argument string
        
    Returns:
        Parsed arguments dict
    """
    if not command_def.get("args"):
        # No args defined, return raw text
        return {"raw": args_text} if args_text else {}
    
    parsed = {}
    remaining = args_text.strip()
    
    for arg in command_def["args"]:
        if not remaining:
            # Set default if available
            if "default" in arg:
                parsed[arg["name"]] = arg["default"]
            break
        
        arg_type = arg.get("type", "string")
        arg_name = arg["name"]
        
        if arg_type == "string":
            # String consumes all remaining text
            parsed[arg_name] = remaining.strip()
            break
        
        elif arg_type == "choice":
            # Match against allowed choices
            choices = arg.get("choices", [])
            matched = False
            
            for choice in choices:
                choice_value = choice if isinstance(choice, str) else choice.get("value")
                if remaining.startswith(choice_value):
                    parsed[arg_name] = choice_value
                    remaining = remaining[len(choice_value):].strip()
                    matched = True
                    break
            
            if not matched and "default" in arg:
                parsed[arg_name] = arg["default"]
        
        elif arg_type == "number":
            # Extract number
            match = re.match(r'(\d+(?:\.\d+)?)', remaining)
            if match:
                parsed[arg_name] = float(match.group(1))
                remaining = remaining[match.end():].strip()
            elif "default" in arg:
                parsed[arg_name] = arg["default"]
        
        elif arg_type == "boolean":
            # Match yes/no, true/false, on/off
            lower = remaining.lower()
            if lower.startswith(("yes", "true", "on", "1")):
                parsed[arg_name] = True
                remaining = remaining[3:].strip()
            elif lower.startswith(("no", "false", "off", "0")):
                parsed[arg_name] = False
                remaining = remaining[2:].strip()
            elif "default" in arg:
                parsed[arg_name] = arg["default"]
    
    return parsed


def build_command_text(command_def: dict, args: Dict[str, Any]) -> str:
    """
    Build command text from args
    
    Matches TypeScript buildCommandTextFromArgs()
    
    Args:
        command_def: Command definition
        args: Parsed arguments
        
    Returns:
        Full command text
    """
    command_name = command_def.get("native_name", command_def.get("key", ""))
    
    if not args or not args.get("values"):
        return f"/{command_name}"
    
    # Build args string
    arg_values = args.get("values", {})
    args_str = " ".join(str(v) for v in arg_values.values() if v is not None)
    
    if args_str:
        return f"/{command_name} {args_str}"
    
    return f"/{command_name}"


def resolve_command_arg_menu(
    command_def: dict,
    current_args: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Resolve which argument needs interactive menu
    
    Returns menu configuration for first unresolved argument
    with choices.
    
    Matches TypeScript resolveCommandArgMenu()
    """
    if not command_def.get("args"):
        return None
    
    for arg in command_def["args"]:
        arg_name = arg["name"]
        
        # Skip if already provided
        if arg_name in current_args:
            continue
        
        # Check if this arg has choices (can show menu)
        if arg.get("type") == "choice" and arg.get("choices"):
            choices_list = []
            
            for choice in arg["choices"]:
                if isinstance(choice, str):
                    choices_list.append({
                        "value": choice,
                        "label": choice.title(),
                    })
                elif isinstance(choice, dict):
                    choices_list.append({
                        "value": choice.get("value", ""),
                        "label": choice.get("label", choice.get("value", "")),
                    })
            
            return {
                "arg": arg,
                "choices": choices_list,
                "title": f"Choose {arg.get('description', arg_name)}",
            }
    
    return None


def validate_command_args(command_def: dict, args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate parsed arguments against command definition
    
    Returns:
        (is_valid, error_message)
    """
    if not command_def.get("args"):
        return True, None
    
    for arg in command_def["args"]:
        arg_name = arg["name"]
        required = arg.get("required", False)
        
        # Check required args
        if required and arg_name not in args:
            return False, f"Missing required argument: {arg_name}"
        
        # Validate type if present
        if arg_name in args:
            value = args[arg_name]
            arg_type = arg.get("type", "string")
            
            if arg_type == "number" and not isinstance(value, (int, float)):
                return False, f"Argument {arg_name} must be a number"
            
            if arg_type == "boolean" and not isinstance(value, bool):
                return False, f"Argument {arg_name} must be true/false"
            
            if arg_type == "choice":
                choices = arg.get("choices", [])
                valid_values = [
                    c if isinstance(c, str) else c.get("value")
                    for c in choices
                ]
                if value not in valid_values:
                    return False, f"Invalid value for {arg_name}. Must be one of: {', '.join(valid_values)}"
    
    return True, None
