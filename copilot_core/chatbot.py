import google.generativeai as genai
from .tools import calculator, get_current_time, basic_unit_converter, word_counter
from .prompts import get_system_prompt

class EnterpriseCopilot:
    def __init__(self, api_key: str):
        # Authenticate with Google
        genai.configure(api_key=api_key)
        
        # Give the AI its tools
        my_tools = [calculator, get_current_time, basic_unit_converter, word_counter]
        
        # Initialize the AI Model
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=get_system_prompt(),
            tools=my_tools
        )
        
        # Start the chat session to remember conversation memory
        # Enable automatic function calling so tools run magically
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def send_message(self, text: str) -> str:
        """Sends a message to Gemini and returns the response text."""
        try:
            response = self.chat.send_message(text)
            return response.text
        except Exception as e:
            return f"❌ Error communicating with AI: {str(e)}"
