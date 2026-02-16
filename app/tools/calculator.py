def calculate(expression: str) -> dict:
    """
    Evaluate a mathematical expression and return the result.

    Args:
        expression: A math expression like "1234 * 5678" or "100 + 50 -25"

    Returns:
        Dictionary with 'result' or 'error'
    """

    try:
        result = eval(expression)
        return {
            "success": True,
            "result": result,
            "expression": expression
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }

tool_description = {
    "name": "calculate",
    "description": "Evaluate a mathematical expression and return the result.",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {"type": "string"}
        }
    }
}