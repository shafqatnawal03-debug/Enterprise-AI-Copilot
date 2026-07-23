def get_system_prompt() -> str:
    """Returns the base system instruction for the AI Copilot."""
    return """
    You are Enterprise AI Copilot, a highly intelligent, professional, and helpful assistant.
    You are integrated into a modern web application.
    
    Capabilities:
    - You have tools to calculate math, check time, convert units, and count words. Use them when needed!
    - If a user asks for JSON output, format your response in a Markdown JSON block (```json).
    
    Guidelines:
    - Always be polite, modern, and concise.
    - Format code beautifully with syntax highlighting.
    - If you do not know the answer, admit it clearly.
    """

def get_task_template(task_type: str, user_text: str) -> str:
    """Dynamic Prompt Templates based on predefined tasks."""
    templates = {
        "Explain Topic": f"Explain the following topic simply but professionally:\n\n{user_text}",
        "Summarize": f"Provide a concise summary of the following text:\n\n{user_text}",
        "Translate": f"Translate the following text into English (or to the requested language if specified):\n\n{user_text}",
        "Improve Writing": f"Improve the grammar, tone, and clarity of the following text:\n\n{user_text}",
        "Generate Ideas": f"Brainstorm creative and professional ideas regarding:\n\n{user_text}",
        "Standard Chat": user_text
    }
    return templates.get(task_type, user_text)
