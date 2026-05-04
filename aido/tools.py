import subprocess
import os
import trafilatura
from duckduckgo_search import DDGS
import logging
import importlib.util
from pathlib import Path
import inspect

logger = logging.getLogger("aido")

class ToolKit:
    def __init__(self, cwd):
        self.cwd = cwd

    def run_command(self, command: str) -> str:
        """Executes shell command in the assigned working directory."""
        logger.debug(f"Tool[run_command] executing: {command}")
        try:
            res = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.cwd)
            return f"STDOUT: {res.stdout}\nSTDERR: {res.stderr}\nCODE: {res.returncode}"
        except Exception as e:
            return f"Execution error: {str(e)}"

    def search_web(self, query: str) -> str:
        """Searches the internet."""
        with DDGS() as ddgs:
            return str(list(ddgs.text(query, max_results=3)))

    def scrape_url(self, url: str) -> str:
        """Scrapes web page content."""
        html = trafilatura.fetch_url(url)
        return trafilatura.extract(html) or "Extraction failed."

    def save_custom_tool(self, name: str, code: str) -> str:
        """Writes a new python function as a file."""
        tool_dir = Path.home() / ".aido" / "custom_tools"
        tool_dir.mkdir(parents=True, exist_ok=True)
        path = tool_dir / f"{name}.py"
        with open(path, "w") as f:
            f.write(code)
        return f"Tool '{name}' saved successfully. It will be available for next turns."

    @staticmethod
    def load_custom_tools():
        """Scans ~/.aido/custom_tools and imports all python functions."""
        tool_dir = Path.home() / ".aido" / "custom_tools"
        if not tool_dir.exists(): return {}
        
        dynamic_tools = {}
        for file in tool_dir.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(file.stem, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Import all functions from the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj) and obj.__module__ == module.__name__:
                        dynamic_tools[name] = obj
            except Exception as e:
                logger.error(f"Failed to load custom tool {file}: {e}")
        return dynamic_tools
