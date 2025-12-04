"""
Example Ingot - A small ingot that processes text and detects numeric content.
Part of the Strategickhaos Ingot Forge system.
"""


def process(data):
    """
    Process input data and return analysis results.

    Args:
        data: Input data to process (will be converted to string)

    Returns:
        dict: Analysis results containing:
            - input: The original input
            - length: Length of the string representation
            - is_numeric: Whether the input contains only digits
    """
    str_data = str(data)
    return {
        "input": data,
        "length": len(str_data),
        "is_numeric": str_data.isdigit()
    }
