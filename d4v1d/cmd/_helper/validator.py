"""
Custom completer - to allow updating
commands on the fly.
"""

from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError

class CmdValidator(Validator):
    """
    Validator for the command prompt
    """

    session: "CmdSession"
    """The command session the validator belongs to."""

    def __init__(self, session: "CmdSession") -> None:
        """
        Initialize a new cmd validator for d4v1d.

        Args:
            session (CmdSession): The session the validator
                belongs to.
        """
        self.session = session
    
    def validate(self, document: Document) -> None:
        """
        Validate some input

        Args:
            document (Document): The input to validate
        """
        if not document.text.strip():
            return
        try:
            self.session[document.text]
        except TypeError as e:
            raise ValidationError(message=str(e))
        except KeyError as e:
            raise ValidationError(message=str(e))
        except ValueError as e:
            raise ValidationError(message=str(e))
