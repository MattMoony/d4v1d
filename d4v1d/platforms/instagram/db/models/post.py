"""
Defines the attributes of an Instagram post.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from d4v1d.platforms.instagram.db.models.location import InstagramLocation
from d4v1d.platforms.instagram.db.models.media import InstagramMedia
from d4v1d.platforms.instagram.db.models.user import InstagramUser
from d4v1d.platforms.platform.mediatype import MediaType


@dataclass
class InstagramPost:
    """
    Represents an Instagram post.
    """

    id: int
    """The instagram post id."""
    short_code: str
    """The instagram post short code."""
    caption: str
    """The instagram post caption."""
    dimensions: Tuple[int, int]
    """The instagram post dimensions."""
    is_video: bool
    """Is this a video?"""
    comments_disabled: bool
    """Are comments disabled?"""
    taken_at: datetime
    """The timestamp when the post was taken."""
    likes: int
    """The number of likes."""

    owner: Optional[InstagramUser] = None
    """The owner of this post; not necessarily set, since loaded & set separately."""
    location: Optional[InstagramLocation] = None
    """The location of this post; not necessarily set, since not always present separately."""

    media_urls: List[Tuple[MediaType, str]] = field(default_factory=list)
    """The media urls of this post."""
    media: List[InstagramMedia] = field(default_factory=list)
    """The media of this post."""

    def dumpj(self) -> Dict[str, Any]:
        """
        Dump the post as a JSON object.
        """
        return {
            'id': self.id,
            'short_code': self.short_code,
            'caption': self.caption,
            'dimensions': {
                'width': self.dimensions[0],
                'height': self.dimensions[1],
            },
            'is_video': self.is_video,
            'comments_disabled': self.comments_disabled,
            'taken_at_timestamp': int(self.taken_at.timestamp()),
            'likes': self.likes,
            'owner': {
                'id': self.owner_id,
            },
            'location': {
                'id': self.location_id,
            },
        }

    def dumpt(self) -> Tuple[Any, ...]:
        """
        Return the post as tuple.
        """
        return (
            self.id,
            self.short_code,
            self.caption,
            self.dimensions[0],
            self.dimensions[1],
            self.is_video,
            self.comments_disabled,
            self.taken_at.isoformat(),
            self.likes,
            self.owner.id if self.owner is not None else None,
            self.location.id if self.location is not None else None,
        )

    @classmethod
    def loadj(cls, obj: Dict[str, Any], api: bool = False) -> "InstagramPost":
        """
        Load a post from a JSON object.

        Args:
            obj (Dict[str, Any]): The JSON object.
            api (bool): Parsing from the API?

        Returns:
            InstagramPost: The parsed instagram post.
        """
        if api:
            p: InstagramPost = InstagramPost(
                obj['id'],
                obj['shortcode'],
                obj['edge_media_to_caption']['edges'][0]['node']['text'],
                (obj['dimensions']['width'], obj['dimensions']['height']),
                obj['is_video'],
                obj['comments_disabled'],
                datetime.fromtimestamp(obj['taken_at_timestamp']),
                obj['edge_media_preview_like']['count'],
                location = InstagramLocation.loadj(obj['location']) if obj['location'] is not None else None,
                media = [ InstagramMedia.loadj(node['node'], api=True) for node in obj['edge_sidecar_to_children']['edges'] ]
                        if 'edge_sidecar_to_children' in obj
                        else [ InstagramMedia.loadj(obj, api=True) ],
            )
            for m in p.media:
                m.post = p
            return p
        return InstagramPost(
            obj['id'],
            obj['short_code'],
            obj['caption'],
            (obj['dimensions']['width'], obj['dimensions']['height']),
            obj['is_video'],
            obj['comments_disabled'],
            datetime.fromtimestamp(obj['taken_at_timestamp']),
            obj['likes'],
            obj['owner']['id'],
        )
