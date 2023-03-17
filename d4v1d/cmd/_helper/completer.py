"""
Custom completer - to allow updating
commands on the fly.
"""

import re
from typing import Iterable, Optional

from prompt_toolkit.completion import (CompleteEvent, Completion,
                                       NestedCompleter)
from prompt_toolkit.completion.nested import NestedDict
from prompt_toolkit.document import Document


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

    def get_completions(self, document: Document, 
                        complete_event: CompleteEvent) -> Iterable[Completion]:
        """
        Overwrite ``prompt_toolkit`` ``get_completion`` method
        in order to allow custom, state-dependend completion for 
        commands.

        Args:
            document (Document): The current input.
            complete_event (CompleteEvent): The event that triggered this.

        Returns:
            Iterable[Completion]: The available completions.
        """
        try:
            x: Completion = next(super().get_completions(document, complete_event))
            yield x
            return
        except StopIteration:
            pass
        # check if current "end" is a command that offers
        # completion
        try:
            c, args = self.session[document.text]
            compl: Optional[NestedDict] = c.completer(self.session.state)
            if not compl:
                return
            # "complex" ``re`` operation's necessary, because
            # the spaces need to be preserved in order for the
            # completer to work properly apparently ...
            for comp in NestedCompleter.from_nested_dict(compl).get_completions(
                            Document(re.search(r'\s+'.join(args)+r'$', document.text).group()), 
                            complete_event):
                yield comp
        except Exception as e:
            pass
