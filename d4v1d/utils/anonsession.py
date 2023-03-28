"""
Defines a class that allows impersonating
common browsers for web requests.
"""

import random
from functools import partialmethod
from typing import Callable

from curl_cffi import requests as req
from curl_cffi.requests.session import BrowserType

from d4v1d.log import log


class AnonSession(req.Session):
    """
    An "anonymous" web browsing session - i.e. a
    session that can impersonate several common web
    browsers.
    """

    shapeshift: bool
    """Whether the session should shapeshift - i.e. change "appearance" with each request."""
    impersonate: BrowserType
    """The current identity of the session - i.e. the browser profile the session is impersonating."""
    
    def __init__(self, *args, shapeshift: bool = False, **kwargs) -> None:
        """
        Initialize a new "anonymous session".
        """
        super().__init__(*args, **kwargs)
        self.shapeshift = shapeshift

    def plastic_surgery(self) -> None:
        """
        Change the session's identity to one of the possible
        options as defined in the ``BrowserType`` enum.
        """
        self.impersonate = random.choice(list(BrowserType))

    def request(self, *args, **kwargs) -> req.Response:
        """
        Make a request using this anonymous session.
        """
        if self.shapeshift:
            self.plastic_surgery()
        log.debug('%sing URL "%s" as "%s" ...', 
                  args[0] if args else kwargs['method'],
                  args[1] if args else kwargs['url'],
                  self.impersonate.name if self.impersonate else 'no-profile')
        return super().request(*args, **kwargs, impersonate=self.impersonate)
    
    head: Callable = partialmethod(request, "HEAD")
    get: Callable = partialmethod(request, "GET")
    post: Callable = partialmethod(request, "POST")
    put: Callable = partialmethod(request, "PUT")
    patch: Callable = partialmethod(request, "PATCH")
    delete: Callable = partialmethod(request, "DELETE")
