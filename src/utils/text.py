def custom_print(text, color_code=32, width=50, border_char="-"):
    """
    Prints the text with a specified color and formats it within a border.
    
    :param text: The text to print.
    :param color_code: ANSI color code for the text color.
    :param width: Width of the output line.
    :param border_char: Character used for the border.
    """
    formatted_text = format_text(text, width, border_char)
    colored_text = print_colored(formatted_text, color_code)
    print(colored_text)

def print_colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def format_text(text, width=50, border_char="-"):
    border_len = (width - len(text)) // 2
    return f"{border_char * border_len}{text}{border_char * (width - len(text) - border_len)}"