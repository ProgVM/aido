import os
import json
import argparse
from pathlib import Path

class Config:
    CONFIG_PATH = Path.home() / ".aido" / "config.json"
    
    def __init__(self):
        self.args = self._parse_args()
        self.data = self._load_config_file()
        
    def _load_config_file(self):
        if self.CONFIG_PATH.exists():
            with open(self.CONFIG_PATH, "r") as f:
                return json.load(f)
        return {}

    def get(self, key, default=None):
        # Priority: CLI Args > Env Vars > Config File > Default
        val = getattr(self.args, key, None)
        if val is not None and val != default: return val
        
        env_val = os.getenv(f"AIDO_{key.upper()}")
        if env_val: return env_val
        
        return self.data.get(key, default)

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="AIDO: Autonomous AI Terminal Agent")
        # Session Management
        parser.add_argument("--session", help="Session name")
        parser.add_argument("--create-session", help="Create new session")
        parser.add_argument("--delete-session", help="Delete a session")
        parser.add_argument("--list-sessions", action="store_true", help="List all sessions")
        
        # Core
        parser.add_argument("prompt", nargs='?', help="The task")
        parser.add_argument("--api-key", help="Gemini API Key")
        parser.add_argument("--model", default="gemini-3.1-flash-lite-preview")
        parser.add_argument("--system-prompt", help="Custom system instruction")
        parser.add_argument("--cwd", default=os.getcwd(), help="Working directory for AI")
        
        # Generation Params
        parser.add_argument("--temp", type=float, default=0.7)
        parser.add_argument("--top-p", type=float, default=0.95)
        parser.add_argument("--top-k", type=int, default=40)
        parser.add_argument("--max-output", type=int, default=2048)
        parser.add_argument("--safety", default="BLOCK_ONLY_HIGH")
        parser.add_argument("--debug", action="store_true")
        
        return parser.parse_args()
