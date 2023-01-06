"""
Some I/O related utility functions
"""

from rich import print
from typing import *

def e(msg: str) -> None:
    """
    Prints an error message
    """
    print(f'[bold red]Error:[/bold red] {msg}')

def w(msg: str) -> None:
    """
    Prints a warning message
    """
    print(f'[bold yellow]Warning:[/bold yellow] {msg}')

def i(msg: str) -> None:
    """
    Prints an info message
    """
    print(f'[bold blue]Info:[/bold blue] {msg}')
