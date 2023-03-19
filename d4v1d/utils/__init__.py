"""
Some simple utility functions like for printing
fancy titles, coloring stuff, etc.
"""

import random
import shutil
from typing import List, Optional

import colorama as cr
from pyfiglet import Figlet

cr.init()

FORE: List[str] = list(vars(cr.Fore).values())
"""List of all of colorama's foreground colors"""
FONTS: List[str] = [ 'smkeyboard', 'small', 'script', '3x5', 'chunky', 'computer', 'fuzzy', ]
"""List of figlet fonts that can be used"""

def rand_color() -> str:
    """
    Select a random foreground color out of all of colorama's
    colors.

    Returns:
        str: The color's escape code.
    """
    return random.choice(FORE)

def random_font() -> str:
    """
    Select a random font out of a pre-selection of figlet
    fonts.

    Returns:
        str: The random font.
    """
    return random.choice(FONTS)

def center_text(s: str, width: Optional[int] = None) -> str:
    """
    Center the given text according to the width.

    Args:
        s (str): The text.
        width (Optional[int], optional): The width. Defaults to terminal width.

    Returns:
        str: The centered text.
    """
    if width is None or width <= 0:
        width = shutil.get_terminal_size().columns
    sp: str = ' ' * (width//2 - max(len(l) for l in s.split('\n'))//2)
    return '\n'.join(sp + l + sp for l in s.split('\n'))

def color_text(s: str) -> str:
    """
    Color the text using a random colors for each char.

    Args:
        s (str): The text to color.

    Returns:
        str: The colored text.
    """
    return ''.join(rand_color()+c for c in list(s)) + cr.Style.RESET_ALL

def title(s: str, color: bool = True, center: bool = True) -> str:
    """
    Generate a title-like string with the given content (i.e.
    Figlet font, nice colors, centering, etc.).

    Args:
        s (str): The title's content.
        color (bool, optional): Color the title? Defaults to True.
        center (bool, optional): Center the title? Defaults to True.

    Returns:
        str: The properly formatted title string.
    """
    s = Figlet(font=random_font()).renderText(s)
    s = center_text(s) if center else s
    s = color_text(s) if color else s
    return s

def hr(c: str = '=', width: Optional[int] = None) -> str:
    """
    Generate a line separator of the given width with the
    given character.

    Args:
        c (str, optional): The character to use. Defaults to '='.
        width (Optional[int], optional): The width. Defaults to terminal width.

    Returns:
        str: The line separator.
    """
    if width is None or width <= 0:
        width = shutil.get_terminal_size().columns
    return c*width
