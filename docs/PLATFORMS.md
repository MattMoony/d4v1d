<p align="center">
  <img alt="d4v1d" src="media/logo.png" width="125" height="125" />
</p>
<h1 align="center">🅳4🆅1🅳 - Platforms</h1>

> This gives an overview of how platforms are implemented in d4v1d - in case you want to add your own.

## 📖 Table of Contents

- [📖 Table of Contents](#-table-of-contents)
- [1️⃣ What are platforms?](#1️⃣-what-are-platforms)
- [2️⃣ How are platforms integrated?](#2️⃣-how-are-platforms-integrated)
- [3️⃣ How are platforms implemented?](#3️⃣-how-are-platforms-implemented)
  - [📊 Info Class](#-info-class)
  - [🚉 Platform class](#-platform-class)
    - [`get_user_description`](#get_user_description)
    - [`get_user_followers`](#get_user_followers)
    - [`get_user_following`](#get_user_following)
    - [`get_user_number_posts`](#get_user_number_posts)
  - [🤖 Bot Class](#-bot-class)
  - [👥 Group Class](#-group-class)
  - [🗃️ Database Class](#️-database-class)
  - [🕹️ Commands Module](#️-commands-module)
    - [`get_cmds`](#get_cmds)
    - [`CLISessionState`](#clisessionstate)
    - [`Command`](#command)

## 1️⃣ What are platforms?

`d4v1d` platforms are a way to **abstract away the differences** between different social-media platforms. They contain all the **logic to interact** with a specific platform, and are used by the `d4v1d` core to interact with the platform / to extract user information.

## 2️⃣ How are platforms integrated?

`d4v1d` is meant to be as extensible as possible, and to allow for **easy addition of new platforms**. To achieve this, platform-specific code is generally implemented in a **separate python module** following the naming convention `d4v1d_p_<PLATFORM-NAME>`.

Only a **few standard platforms** that ship with `d4v1d` are implemented in the main `d4v1d` repository (under `platforms/`). All other platforms should be implemented in **separate repositories**, and installed as python packages.

## 3️⃣ How are platforms implemented?

Each platform module has to be structured in the way that the model `platform` platform is structured.

### 📊 Info Class

> `d4v1d.platforms.platform.info.Info`

This class is used to wrap the information that is retrieved from the platform. It contains the following attributes:

```md
- value (Any): The information
- date (datetime): The date of the information
- platform (Platform): The platform
```

This class has been introduced, because it seems rather reasonable to assume that the information retrieved from a platform is **not static**, but rather **changes over time**.

### 🚉 Platform class

> `d4v1d.platforms.platform.Platform`

Every platform **needs to extend this class**, and implement at least the following methods, since `d4v1d` makes use of them, to allow for some sort of **cross-platform data collection & analysis**:

#### `get_user_description`

> `get_user_description (cls, username: str) -> d4v1d.platforms.platform.info.Info<str>`

Get a brief summary of the user - usually something like a bio exists, in which case, this can simply be returned.

#### `get_user_followers`

> `get_user_followers (cls, username: str) -> d4v1d.platforms.platform.info.Info<List[str]>`

Get a list of the usernames of all the users' followers. These usernames can then be used to get more information about the followers, and so on.

#### `get_user_following`

> `get_user_following (cls, username: str) -> d4v1d.platforms.platform.info.Info<List[str]>`

Get a list of the usernames of all users that the specified user follows. Just like the usernames retrieved with `get_user_followers`, these usernames can then be used to get more information, ...

#### `get_user_number_posts`

> `get_user_number_posts (cls, username: str) -> d4v1d.platforms.platform.info.Info<int>`

Get the number of posts that the user has made.

### 🤖 Bot Class

> `d4v1d.platforms.platform.bot.Bot`

### 👥 Group Class

> `d4v1d.platforms.platform.bot.Group`

### 🗃️ Database Class

> `d4v1d.platforms.platform.db.Database`

### 🕹️ Commands Module

> `d4v1d.platforms.platform.cmd`

The commands module contains all the commands that are available for the platform. These commands are then used by the `d4v1d` core to grant the user access to them.

#### `get_cmds`

> `get_cmds () -> Dict[str, Any]`

This method returns a dictionary containing all the commands that are available for the platform. The keys of the dictionary are the names of the commands, and the values are the actual commands (= instances of subclasses of the `d4v1d.platforms.platform.cmd.Command` class).

It is used by the `d4v1d` upon switching to a platform environment using the `use` command, to get all the commands that are available for the platform.

#### `CLISessionState`

> `class CLISessionState (object)`

This class is used to keep track of the current state of the CLI session (as the name would suggest). It contains the following attributes:

```md
- platform (Platform): The platform that is currently being used
```

#### `Command`

> `class Command (object)`

This class is the base class for all commands that are available for a platform - actually, it's also used as the base for all regular `d4v1d` commands. It's initialized with the following arguments:

```python
def __init__(self, name: str, aliases: List[str] = [], description: str = ''):
    """
    Initializes a command with the specified name, aliases and description.

    Args:
        name (str): The name of the command
        aliases (List[str], optional): The aliases of the command. Defaults to [].
        description (str, optional): The description of the command. Defaults to ''.
    """
    # ...
```

It only really defines one method - `execute` - which, as the name suggests, is used to execute the command. It is called with the list of arguments passed to it in the CLI and the current `CLISessionState`. The base `Command` class also implements the python magic function `__call__`, which simply calls `execute` with the passed arguments.

```python
def execute(self, args: List[str], state: CLISessionState) -> None:
    """
    Executes the command with the specified arguments.
    """
    # ...

def __call__(self, args: List[str], state: CLISessionState) -> None:
    """
    Calls the execute method.
    """
    # ...
```

All a specific command needs to do is to initialize the `Command` object in `__init__` and **override the `execute` method** - e.g. this is what the `exit` command looks like:

```python
class Exit(Command):
    """
    The exit command
    """

    def __init__(self):
        """
        Initializes the exit command
        """
        super().__init__('exit', aliases=['quit',], description='Exits the program')

    def execute(self, args: List[str], state: CLISessionState) -> None:
        """
        Executes the exit command
        """
        sys.exit(0)
```

---

[⬆️ Back to top](#table-of-contents)

... m4ttm00ny (December 2022)
