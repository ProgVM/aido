import json
import logging
import shutil
from pathlib import Path
from google.genai import types

logger = logging.getLogger("aido")

class MemoryManager:
    def __init__(self):
        self.base_dir = Path.home() / ".aido" / "sessions"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.last_session_file = Path.home() / ".aido" / "last_session.txt"

    def get_active_session(self, requested=None):
        if requested:
            self.set_last_session(requested)
            return requested
        if self.last_session_file.exists():
            return self.last_session_file.read_text().strip()
        return "default"

    def set_last_session(self, name):
        self.last_session_file.write_text(name)

    def load_history(self, session_name):
        path = self.base_dir / f"{session_name}.json"
        if not path.exists():
            return []
            
        try:
            with open(path, "r") as f:
                data = json.load(f)
                # Reconstruct types.Content objects from dictionaries
                return [types.Content(**item) for item in data]
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Session file corrupted: {e}. Moving to backup and starting fresh.")
            # Backup corrupted file
            shutil.move(path, path.with_suffix(".json.bak"))
            return []
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            return []

    def save_history(self, session_name, history):
        path = self.base_dir / f"{session_name}.json"
        try:
            # Using mode='json' converts complex objects and bytes 
            # into JSON-compatible formats (bytes -> base64 strings)
            data = [item.model_dump(mode='json') for item in history]
            
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def delete_session(self, name):
        path = self.base_dir / f"{name}.json"
        if path.exists():
            path.unlink()
