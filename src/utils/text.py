def custom_print(text, color_code=32, width=50, border_char="-", end="\n"):
    """
    Prints the text with a specified color and formats it within a border.
    
    :param text: The text to print.
    :param color_code: ANSI color code for the text color.
    :param width: Width of the output line.
    :param border_char: Character used for the border.
    """
    formatted_text = format_text(text, width, border_char)
    colored_text = print_colored(formatted_text, color_code)
    print(colored_text, end=end)

def print_colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def format_text(text, width=50, border_char="-"):
    border_len = (width - len(text)) // 2
    return f"{border_char * border_len}{text}{border_char * (width - len(text) - border_len)}"


def colorize_text(text: str, color: str = "reset") -> str:
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "reset": "\033[0m"
    }
    color_code = colors.get(color.lower(), colors["reset"])
    return f"{color_code}{text}{colors['reset']}"
