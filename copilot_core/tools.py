import datetime

def calculator(a: float, b: float, operator: str) -> float:
    """A calculator tool for basic arithmetic operations (+, -, *, /)."""
    if operator == '+': return a + b
    if operator == '-': return a - b
    if operator == '*': return a * b
    if operator == '/': return a / b if b != 0 else 0.0
    return 0.0

def get_current_time() -> str:
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def basic_unit_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Converts a value from one unit to another (celsius, fahrenheit, km, miles)."""
    f, t = from_unit.lower(), to_unit.lower()
    if f == "celsius" and t == "fahrenheit": return (value * 9/5) + 32
    if f == "fahrenheit" and t == "celsius": return (value - 32) * 5/9
    if f == "km" and t == "miles": return value * 0.621371
    if f == "miles" and t == "km": return value / 0.621371
    return value

def word_counter(text: str) -> int:
    """Counts the number of words in a given text string."""
    return len(text.split())
