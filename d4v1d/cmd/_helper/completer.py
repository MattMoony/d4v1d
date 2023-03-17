"""
Custom completer - to allow updating
commands on the fly.
"""

from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion.nested import NestedDict

class CmdCompleter(NestedCompleter):
    """
    Custom completer - to allow updating
    commands on the fly.
    """

    session: "CmdSession"
    """The command session the completer belongs to."""

    def update(self, data: NestedDict) -> None:
        """
        Update the completer with new commands.

        Args:
            data (NestedDict): The new commands
        """
        self.options = NestedCompleter.from_nested_dict(data).options
