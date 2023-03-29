"""
Defines the attributes of an Tellonym tell.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from d4v1d.platforms.tellonym.db.models.user import TellonymUser


@dataclass
class TellonymTell:
    """
    Represents an Tellonym tell.
    """

    postType: int
    """The tellonym tell type."""
    id: int
    """The tellonym tell id."""
    answer: str
    """The tellonym tell answer."""
    likesCount: int
    """The tellonym tell likes."""
    createdAt: datetime
    """The timestamp when the tell was created."""
    tell: str
    """The tellonym tell."""

    owner: Optional[TellonymUser] = None
    """The owner of this post; not necessarily set, since loaded & set separately."""

    def dumpj(self) -> Dict[str, Any]:
        """
        Dump the tell as a JSON object.
        """
        return {
            'postTye': self.postType,
            'id': self.id,
            'answer': self.answer,
            'likesCount': self.likesCount,
            'createdAt': self.createdAt.timestamp(),
            'tell': self.tell,
            'owner': {
                'id': self.owner.id
            }
        }

    def dumpt(self) -> Tuple[Any, ...]:
        """
        Return the post as tuple.
        """
        return (
            self.postType,
            self.id,
            self.answer,
            self.likesCount,
            self.createdAt,
            self.tell,
            self.owner.id if self.owner is not None else None,
        )

    @classmethod
    def loadj(cls, obj: Dict[str, Any], api: bool = False) -> "TellonymTell":
        """
        Load a tell from a JSON object.

        Args:
            obj (Dict[str, Any]): The JSON object.
            api (bool): Parsing from the API?

        Returns:
            TellonymTell: The parsed tellonym tell.
        """
        if api:
            t: TellonymTell = TellonymTell(postType=obj['postType'], id=obj['id'], answer=obj['answer'],
                                           likesCount=obj['likesCount'], createdAt=obj['createdAt'], tell=obj['tell'])
            return t
        return TellonymTell(**obj)

    @classmethod
    def loadt(cls, obj: Tuple[Any, ...]) -> "TellonymTell":
        """
        Load a tell from a tuple
        """
        return TellonymTell(*obj)
