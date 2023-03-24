"""
Defines the attributes of Instagram media.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from d4v1d.platforms.platform.mediatype import MediaType


@dataclass
class InstagramMedia:
    """
    Represents some sort of media on Instagram.
    """
    
    id: int
    """The media's id."""
    type: MediaType
    """The type of media."""
    url: str
    """The remote url of the media."""
    dimensions: Tuple[int, int]
    """The dimensions of the media."""

    path: Optional[str] = None
    """The local path of the media (if it has been downloaded)."""
    post: Optional["InstagramPost"] = None
    """The post this media belongs to; possibly not set, since loaded & set separately."""

    def dumpj(self) -> dict:
        """
        Dump the media as a JSON object.
        """
        return {
            'id': self.id,
            'post': self.post.id if self.post is not None else None,
            'type': self.type.value,
            'url': self.url,
            'path': self.path,
            'dimensions': {
                'width': self.dimensions[0],
                'height': self.dimensions[1],
            },
        }
    
    def dumpt(self) -> tuple:
        """
        Dump the media as a tuple.
        """
        return (
            self.id,
            self.post.id if self.post is not None else None,
            self.type.value,
            self.url,
            self.path,
            *self.dimensions,
        )
    
    @classmethod
    def loadj(cls, data: dict, api: bool = False, post: Optional["InstagramPost"] = None) -> 'InstagramMedia':
        """
        Load the media from a JSON object.

        Args:
            data (dict): The JSON object.
            api (bool): Whether the data is from the API or not.
            post (Optional[InstagramPost]): The post this media belongs to.

        Returns:
            InstagramMedia: The parsed media.
        """
        if api:
            return cls(
                data['id'],
                MediaType.IMAGE if not data['is_video'] else MediaType.VIDEO,
                data['display_url'] if not data['is_video'] else data['video_url'],
                (data['dimensions']['width'], data['dimensions']['height']),
                post = post,
            )
        return cls(
            data['id'],
            MediaType(data['type']),
            data['url'],
            (data['dimensions']['width'], data['dimensions']['height']),
            data['path'],
            post = post,
        )
