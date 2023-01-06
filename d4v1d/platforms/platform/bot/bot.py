"""
Contains the definition of the Bot class,
i.e. an automated user / anonymous browser of 
the target social-media platform.
"""

class Bot(object):
    """
    Template bot class - template automated user.
    """
    
    group: "Group"
    """The group the bot belongs to"""
    anonymous: bool
    """Whether or not the bot is an authenticated user"""
    requests: int
    """The number of requests the bot has made"""

    def __init__(self, group: "Group", anonymous: bool):
        """
        Creates a new Bot object

        Args:
            group (Group): The group the bot belongs to
            anonymous (bool): Whether the bot should be anonymous
        """
        self.group = group
        self.anonymous = anonymous
        self.requests = 0
