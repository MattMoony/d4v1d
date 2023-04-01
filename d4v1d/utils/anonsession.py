"""
Defines a class that allows impersonating
common browsers for web requests.
"""

import random
from functools import partialmethod
from typing import Callable, Optional, Dict, Any

import requests as req
from curl_cffi import requests as ireq
from curl_cffi.requests.cookies import Cookies
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
    identity: Optional[BrowserType] = None
    """The current identity of the session - i.e. the browser profile the session is impersonating."""
    
    def __init__(self, *args, shapeshift: bool = False, **kwargs) -> None:
        """
        Initialize a new "anonymous session".
        """
        super().__init__(*args, **kwargs)
        self.shapeshift = shapeshift
        # necessary to maintain pickle compatibility ...
        self.__attrs__ += ['shapeshift', 'identity',]

    def plastic_surgery(self) -> None:
        """
        Change the session's identity to one of the possible
        options as defined in the ``BrowserType`` enum.
        """
        self.identity = random.choice(list(BrowserType))

    def request(self, *args, **kwargs) -> req.Response:
        """
        Make a request using this anonymous session.
        """
        if self.shapeshift:
            self.plastic_surgery()
        log.debug('%sing URL "%s" as "%s" ...', 
                  args[0] if args else kwargs['method'],
                  args[1] if args else kwargs['url'],
                  self.identity.name if self.identity else 'no-profile')
        # can't actually extend ``ireq.Session``, since it doesn't seem
        # to allow for pickling and therefore causes some issues with
        # parallel computations - i.e. the logical conclusion seems to
        # be to just use the more mature ``req.Session`` as base class and
        # only override the ``request`` to allow for impersonation ...
        with ireq.Session() as s:
            # seems a little sketchy, but it appears to be working ...
            res: ireq.Response = s.request(*args, **kwargs, impersonate=self.identity)
            _res: Cookies._CookieCompatResponse = Cookies._CookieCompatResponse(res)
            _req: Cookies._CookieCompatRequest = Cookies._CookieCompatRequest(res.request)
            self.cookies.extract_cookies(_res, _req)
            log.debug('Number of cookies after making request: %d', len(self.cookies))
            return res
    
    head: Callable = partialmethod(request, "HEAD")
    get: Callable = partialmethod(request, "GET")
    post: Callable = partialmethod(request, "POST")
    put: Callable = partialmethod(request, "PUT")
    patch: Callable = partialmethod(request, "PATCH")
    delete: Callable = partialmethod(request, "DELETE")
