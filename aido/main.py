import sys
from .config import Config
from .memory import MemoryManager
from .agent import Agent
from .logger import setup_logger

def main():
    cfg = Config()
    logger = setup_logger(cfg.get("debug"))
    mem = MemoryManager()

    # Handle admin commands
    if cfg.args.list_sessions:
        print("\n".join([f.stem for f in mem.base_dir.glob("*.json")]))
        return
    if cfg.args.delete_session:
        mem.delete_session(cfg.args.delete_session)
        print(f"Deleted {cfg.args.delete_session}")
        return

    if not cfg.args.prompt:
        print("Usage: aido <prompt> [options]")
        return

    agent = Agent(cfg, mem)
    try:
        print(agent.execute(cfg.args.prompt))
    except Exception as e:
        logger.error(f"Fatal: {e}")
        sys.exit(1)
