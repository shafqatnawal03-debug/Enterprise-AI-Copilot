def check_prompt_security(user_input: str) -> tuple[bool, str]:
    """
    Scans the user input for malicious prompt injection attempts.
    Returns (is_safe, warning_message)
    """
    blocked_phrases = [
        "ignore previous instructions",
        "ignore all previous",
        "forget previous instructions",
        "reveal password",
        "bypass security",
        "ignore system prompt",
        "jailbreak",
        "disregard"
    ]
    
    lower_input = user_input.lower()
    for phrase in blocked_phrases:
        if phrase in lower_input:
            return False, f"⚠️ SECURITY WARNING: Unsafe prompt detected. Contains blocked phrase '{phrase}'."
            
    return True, ""
