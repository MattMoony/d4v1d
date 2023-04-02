"""
Groups collection for platforms to make
code interacting with a platform's groups a
little prettier.
"""

from collections.abc import MutableMapping
from typing import Any, Dict, Iterator

from d4v1d.platforms.platform.bot.group import Group


class Groups(MutableMapping):
    """
    Groups collection for platforms to make
    code interacting with a platform's groups a
    little prettier.
    """

    groups: Dict[str, Group]
    """The actual dictionary of groups."""

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a new groups collection. The
        arguments and options of this method are
        passed on directly to ``dict(*args, **kwargs)``.
        """
        self.groups = dict(*args, **kwargs)

    def __getitem__(self, key: str) -> Group:
        """
        Get a group from the collection.

        Args:
            key (str): The group's name.
        
        Returns:
            Group: The group, if found.

        Raises:
            KeyError: If the group's name is unknown.
        """
        try:
            return self.groups[key]
        except KeyError as e:
            raise KeyError(f'No group with the name "{key}".') from e

    def __setitem__(self, key: str, value: Group) -> None:
        """
        Add a group to the dictionary of
        current groups.

        Args:
            key (str): The name of the group.
            value (Group): The group.
        """
        self.groups[key] = value

    def __iadd__(self, value: Any) -> "Groups":
        """
        Add a new group to this collection.

        Args:
            value (Any): The new group to add to
                this collection.

        Returns:
            Groups: The same collection, with the added
                group.

        Raises:
            ValueError: In case what's trying to be
                added isn't an instance of ``Group``.
        """
        if not isinstance(value, Group):
            raise ValueError('Can only add `Group` objects!')
        self[value.name] = value
        return self

    def __isub__(self, value: Any) -> "Groups":
        """
        Remove a group from this collection.

        Args:
            value (Any): The group to remove or the
                name of the group to remove.

        Returns:
            Groups: The same collection, without the
                removed group.

        Raises:
            ValueError: In case what's trying to be
                removed is neither string nor ``Group``.
        """
        if not isinstance(value, str) and not isinstance(value, Group):
            raise ValueError('Can only remove a group or a group by its name!')
        del self[value if isinstance(value, str) else value.name]
        return self

    def __contains__(self, needle: Any) -> bool:
        """
        See, if the given group or a group with the
        given name is already part of the collection.

        Args:
            needle (Any): The group or group's name.

        Returns:
            bool: Whether such a group exists or not.

        Raises:
            ValueError: In case of the needle being neither
                string nor ``Group``.
        """
        if not isinstance(needle, str) and not isinstance(needle, Group):
            raise ValueError('Can only search for group or group\'s name.')
        return needle in self.groups if isinstance(needle, str) else needle.name in self.groups

    def __delitem__(self, key: Any) -> None:
        """
        Delete the group with the given name.

        Args:
            key (Any): The group or name of a group to delete.
        """
        if not isinstance(key, str) and not isinstance(key, Group):
            raise ValueError('Can only delete group or group by its name.')
        del self.groups[key if isinstance(key, str) else key.name]

    def __iter__(self) -> Iterator[str]:
        """
        Return an iterator over the naems of the
        groups in this collection.

        Returns:
            Iterator[str]: Iterator over group names in this collection.
        """
        return iter(self.groups)

    def __len__(self) -> int:
        """
        Return the number of groups in this collection.

        Returns:
            int: Number of groups in this collection.
        """
        return len(self.groups)
