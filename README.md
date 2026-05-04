# AIDO: Autonomous AI Terminal Agent

AIDO is an advanced command-line interface (CLI) agent powered by Google Gemini. It bridges the gap between natural language commands and system execution, transforming your terminal into an intelligent workspace that can automate tasks, browse the web, and grow its own capabilities.

## Key Features

*   **Self-Development**: AIDO can write its own Python tools (`.py` files), save them, and dynamically load/execute them in the same session.
*   **Persistent Context**: Remembers conversation history across runs using dedicated session files.
*   **Hierarchical Configuration**: Supports CLI arguments, environment variables, and a local JSON configuration file.
*   **Autonomous Tooling**: Built-in capabilities for shell command execution, real-time web search (DuckDuckGo), and URL scraping (Trafilatura).
*   **Session Management**: Create, list, switch, and delete workspaces to keep tasks organized.

## Installation

1. Clone the repository.
2. Install the package in editable mode to allow CLI access:

```bash
pip install -e .
```

You can also install the package with:

```bash
pip install aido-cli
```

## Configuration

AIDO uses a hierarchical configuration system. If a parameter is set in multiple places, the priority is:
1. **CLI Argument** (e.g., `--temp 0.5`)
2. **Environment Variable** (e.g., `AIDO_TEMP=0.5`)
3. **Config File** (`~/.aido/config.json`)
4. **Default Value**

### Environment Variables
Set these in your `.bashrc` or `.zshrc`:
* `GEMINI_API_KEY`: Your API key from Google AI Studio.
* `AIDO_MODEL`: Default model (e.g., `gemini-2.5-flash`).

### Configuration File
Create `~/.aido/config.json` to store your permanent preferences:
```json
{
    "model": "gemini-2.5-flash",
    "temp": 0.7,
    "safety": "BLOCK_ONLY_HIGH"
}
```

## Usage

### Basic Interaction
```bash
aido "List all python files in the current folder and count lines of code"
```

### Managing Sessions
AIDO automatically saves history to the last used session.
* **Start/Resume a specific session**:
  ```bash
  aido "Continue working on the web scraper" --session web_scraper_dev
  ```
* **List existing sessions**:
  ```bash
  aido --list-sessions
  ```
* **Delete a session**:
  ```bash
  aido --delete-session old_project
  ```

### Advanced Settings
* **Debug Mode**: See exactly what the AI is doing.
  ```bash
  aido "Analyze the system load" --debug
  ```
* **Change System Identity**:
  ```bash
  aido "Refactor this code" --system-prompt "You are an expert Python architect."
  ```

## The Self-Development Mechanism

AIDO can write its own functionality. When you ask it to "create a tool to check system uptime," it will use the `save_custom_tool` function.

1. **Generation**: The agent writes a Python script to `~/.aido/custom_tools/`.
2. **Dynamic Discovery**: On every turn, the `ToolKit` scans that folder and imports any new functions found.
3. **Execution**: The agent immediately recognizes the new function as an available tool and can call it without restarting the script.

*Note: If the AI creates a tool, ensure it writes valid Python code with necessary imports (e.g., `import os`). If it fails, simply tell it: "The tool you created is missing an import, please fix it."*

## File Structure

Everything is organized in your home directory:

*   `~/.aido/`
    *   `config.json` : Your permanent settings.
    *   `last_session.txt` : Tracks the session used in the last run.
    *   `sessions/` : JSON files containing your chat history.
    *   `custom_tools/` : AI-generated Python scripts.

## Troubleshooting

*   **"Failed to load history"**: This usually means the JSON file was corrupted (e.g., interrupted write). AIDO will automatically backup the corrupted file as `.bak` and reset to a clean state.
*   **"Tool not found"**: If the AI says it created a tool but can't see it, check `~/.aido/custom_tools/` to see if the file was actually written.
*   **Dependencies**: Ensure `trafilatura` and `duckduckgo-search` are installed via `pip`.
