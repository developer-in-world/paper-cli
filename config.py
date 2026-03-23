import json
import os
import sys
import stat
from pathlib import Path

CONFIG_FILE = Path.home() / '.paper_cli_config.json'

def get_config() -> dict:
    """"Reads the configuration file securely."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}

def _secure_file_permissions(filepath: Path):
    """Sets strict file permissions (cross-platform).
    - Unix/macOS: chmod 600 (owner read/write only)
    - Windows: Uses icacls to restrict access to the current user only
    """
    if sys.platform == 'win32':
        import subprocess
        username = os.environ.get('USERNAME', '')
        if username:
            try:
                subprocess.run(
                    ['icacls', str(filepath), '/inheritance:r',
                     '/grant:r', f'{username}:(R,W)'],
                    capture_output=True, check=True
                )
            except Exception:
                pass  # Non-critical; best-effort on Windows
    else:
        os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)

def save_config(config: dict):
    """"Saves configuration securely with strict permissions."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    _secure_file_permissions(CONFIG_FILE)

def get_api_key(key_name: str, prompt_message: str) -> str:
    """"Retrieves an API key, or securely prompts user."""
    config = get_config()
    if key_name in config and config[key_name]:
        return config[key_name]
    
    import getpass
    print(f"\n[Configuration Required] {prompt_message}")
    value = getpass.getpass(f"Enter {key_name} (or press Enter to skip): ").strip()
    
    if value:
        config[key_name] = value
        save_config(config)
        
    return value
