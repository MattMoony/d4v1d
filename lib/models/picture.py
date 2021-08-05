import os, magic
import requests as req
from typing import *

class Picture(object):
    """An arbitrary picture - either from the web, disk, memory, ..."""

    def __init__(self, url: Optional[str] = None, data: Optional[bytes] = None, path: Optional[str] = None, headers: Optional[str] = None):
        self.path: Optional[str] = path
        self.__url: Optional[str] = url
        self.__data: Optional[bytes] = data
        self.__path: Optional[str] = path
        self.headers: Optional[str] = headers
        if not (url or data or path):
            raise Exception('Cannot initialize picture without any information!')

    def __iadd__(self, other: Union["Picture", bytes]):
        """Add content to the image (e.g. when downloading multiple chunks)"""
        if type(other) == bytes:
            self.__data += other
        elif type(other) == Picture:
            self.__data += other.__data

    def raw(self) -> bytes:
        """Get the picture's raw bytes"""
        if self.__data:
            return self.__data
        elif self.__url:
            return req.get(self.__url, headers=self.headers).content
        elif self.__path:
            with open(self.__path, 'rb') as f:
                return f.read()
        return b''

    def ext(self) -> str:
        """Get the picture's appropriate extension"""
        if self.__url:
            return os.path.splitext(self.__url.split('?')[0])[1]
        elif self.__path:
            return os.path.splitext(self.__path)[1]
        elif self.__data:
            return magic.from_buffer(self.__data).split()[0].lower()

    def write(self, path: str) -> None:
        """Store the image on the hard disk"""
        with open(path, 'wb') as f:
            f.write(self.raw())
