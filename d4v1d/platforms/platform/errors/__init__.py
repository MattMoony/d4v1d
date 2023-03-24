"""
Module containing Exceptions that can be
raised by platforms.
"""

class PlatformError(Exception):
    """
    Generic exception for platforms
    """

    def __str__(self) -> str:
        """
        Get string representation of the exception.

        Returns:
            str: The string representation of the exception
        """
        return f'{self.__class__.__name__}: {self.args[0]}'

class EmptyGroupError(PlatformError):
    """
    Thrown, when no bots have been assigned
    to a group, but the group is asked to
    perform a task
    """

class NoGroupsError(PlatformError):
    """
    Thrown, when no groups of bots have been
    created for a platform
    """

class UnknownUserError(PlatformError):
    """
    Thrown, when a user is not known to the
    platform
    """

class BadAPIResponseError(PlatformError):
    """
    Thrown, when the API responds in an
    unexpected way or doesn't respond at all
    """

class RateLimitError(BadAPIResponseError):
    """
    Thrown, when the API responds with a
    rate limit error
    """

class RequiresAuthenticationError(BadAPIResponseError):
    """
    Thrown, when an action requires
    authentication, but the bot is anonymous
    """
