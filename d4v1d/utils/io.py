"""
Some I/O related utility functions
"""

from rich import print
from typing import *

def e(msg: str) -> None:
    """
    Prints an error message
    """
    print(_e(msg))

def _e(msg: str) -> None:
    """
    Marks up an error message as if outputting it.
    """
    return f'[bold red]Error:[/bold red] {msg}'

def w(msg: str) -> None:
    """
    Prints a warning message
    """
    print(_w(msg))

def _w(msg: str) -> None:
    """
    Marks up a warning message as if outputting it.
    """
    return f'[bold yellow]Warning:[/bold yellow] {msg}'

def i(msg: str) -> None:
    """
    Prints an info message
    """
    print(_i(msg))

def _i(msg: str) -> None:
    """
    Marks up an info message as if outputting it.
    """
    return f'[bold blue]Info:[/bold blue] {msg}'

def l(msg: str) -> None:
    """
    Outputs a single line to the user. 
    """
    print(_l(msg))

def _l(msg: str) -> None:
    """
    Marks up a single line as if outputting it.
    """
    return f'[bold grey53][*][/bold grey53] {msg}'

def _(msg: str) -> None:
    """
    Output an *indented* line.
    """
    print(__(msg))

def __(msg: str) -> None:
    """
    Marks up an *indented* line as if outputting it.
    """
    return f'    └── {msg}'
