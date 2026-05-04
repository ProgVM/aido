import logging
from google import genai
from google.genai import types
from .tools import ToolKit

logger = logging.getLogger("aido")

class Agent:
    def __init__(self, config, memory):
        self.config = config
        self.memory = memory
        self.client = genai.Client(api_key=config.get("api_key"))
        self.tools = ToolKit(config.get("cwd"))
        
        self.root_instruction = (
            "You are AIDO, an autonomous terminal agent. "
            f"Your current working directory is: {config.get('cwd')}. "
            "You have tools for system interaction, web search, and file scraping. "
            "IMPORTANT: When using 'save_custom_tool' to write new Python tools, "
            "always include all necessary import statements (e.g., 'import os', 'import sys') "
            "inside the code block you generate. If your tool fails, analyze the error and "
            "rewrite it to fix dependencies or logic."
        )

    def _get_all_tools(self):
        """Combines static tools and dynamically loaded custom tools."""
        registry = {
            "run_command": self.tools.run_command,
            "search_web": self.tools.search_web,
            "scrape_url": self.tools.scrape_url,
            "save_custom_tool": self.tools.save_custom_tool
        }
        
        # Load dynamic ones
        dynamic = self.tools.load_custom_tools()
        registry.update(dynamic)
        return registry

    def execute(self, prompt: str):
        session_name = self.memory.get_active_session(self.config.get("session"))
        history = self.memory.load_history(session_name)
        
        # Get the full registry
        tool_registry = self._get_all_tools()
        
        chat = self.client.chats.create(
            model=self.config.get("model", "gemini-2.5-flash"),
            config=types.GenerateContentConfig(
                system_instruction=self.root_instruction,
                tools=list(tool_registry.values())
            ),
            history=history
        )
        
        response = chat.send_message(prompt)
        
        # Loop to process tool calls
        while response.parts and response.parts[0].function_call:
            fn = response.parts[0].function_call
            fn_name = fn.name
            
            logger.info(f"AI requested tool: {fn_name}")
            
            if fn_name in tool_registry:
                try:
                    result = tool_registry[fn_name](**fn.args)
                    # If we just saved a new tool, refresh registry for next iteration
                    if fn_name == "save_custom_tool":
                        tool_registry = self._get_all_tools()
                except Exception as e:
                    result = f"Error: {str(e)}"
            else:
                result = "Error: Tool not found."
            
            response = chat.send_message(
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": result}
                )
            )
        
        self.memory.save_history(session_name, chat.get_history())
        return response.text
