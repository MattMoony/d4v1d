import os, magic
import requests as req
from typing import *

class Media(object):
    """An arbitrary picture/video/... - either from the web, disk, memory, ..."""

    def __init__(self, name: Optional[str] = None, caption: Optional[str] = None, tagged: List["User"] = [],
                 likes: Optional[int] = None, dislikes: Optional[int] = None,
                 url: Optional[str] = None, data: Optional[bytes] = None, path: Optional[str] = None, headers: Optional[str] = None):
        self.name: Optional[str] = name
        self.caption: Optional[str] = caption
        self.tagged: List["User"] = tagged
        self.likes: Optional[int] = likes
        self.dislikes: Optional[int] = dislikes
        self.__url: Optional[str] = url
        self.__data: Optional[bytes] = data
        self.__path: Optional[str] = path
        self.headers: Optional[str] = headers
        if not (url or data or path):
            raise Exception('Cannot initialize media without any information!')

    def __iadd__(self, other: Union["Media", bytes]):
        """Add content to the media (e.g. when downloading multiple chunks)"""
        if type(other) == bytes:
            self.__data += other
        elif type(other) == Media:
            self.__data += other.__data

    def download(self, session: Optional[req.Session] = None, headers: Optional[Dict[str, Any]] = None) -> None:
        """Downloads the image if necessary"""
        if not self.__url:
            return
        self.__data = (session or req).get(self.__url, headers=(headers or self.headers))

    def raw(self) -> bytes:
        """Get the media's raw bytes"""
        if self.__data:
            return self.__data
        elif self.__url:
            return req.get(self.__url, headers=self.headers).content
        elif self.__path:
            with open(self.__path, 'rb') as f:
                return f.read()
        return b''

    def ext(self) -> str:
        """Get the media's appropriate extension"""
        if self.__data:
            return magic.from_buffer(self.__data).split()[0].lower()
        elif self.__url:
            return os.path.splitext(self.__url.split('?')[0])[1]
        elif self.__path:
            return os.path.splitext(self.__path)[1]

    def write(self, path: str) -> None:
        """Store the media on the hard disk"""
        with open(path, 'wb') as f:
            f.write(self.raw())
