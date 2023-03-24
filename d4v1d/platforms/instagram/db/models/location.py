"""
Defines the attribute of an Instagram location.
"""

from dataclasses import dataclass

@dataclass
class InstagramLocation:
    """
    Represents a location on Instagram.
    """

    id: int
    """The location's id."""
    has_public_page: bool
    """Does this location have a public page?"""
    name: str
    """The location's name."""
    slug: str
    """The location's slug."""

    def dumpj(self) -> dict:
        """
        Dump the location as a JSON object.
        """
        return {
            'id': self.id,
            'has_public_page': self.has_public_page,
            'name': self.name,
            'slug': self.slug,
        }
    
    def dumpt(self) -> tuple:
        """
        Dump the location as a tuple.
        """
        return (
            self.id,
            self.has_public_page,
            self.name,
            self.slug,
        )
    
    @classmethod
    def loadj(cls, obj: dict) -> "InstagramLocation":
        """
        Load a location from a JSON object.
        """
        return InstagramLocation(
            obj['id'],
            obj['has_public_page'],
            obj['name'],
            obj['slug'],
        )
