# Platforms

> This gives an overview of how platforms are implemented in d4v1d - in case you want to add your own.

## 1️⃣ What are platforms?

`d4v1d` platforms are a way to **abstract away the differences** between different social-media platforms. They contain all the **logic to interact** with a specific platform, and are used by the `d4v1d` core to interact with the platform / to extract user information.

## 2️⃣ How are platforms integrated?

`d4v1d` is meant to be as extensible as possible, and to allow for **easy addition of new platforms**. To achieve this, platform-specific code is generally implemented in a **separate python module** following the naming convention `d4v1d_p_<PLATFORM-NAME>`.

Only a **few standard platforms** that ship with `d4v1d` are implemented in the main `d4v1d` repository (under `platforms/`). All other platforms should be implemented in **separate repositories**, and installed as python packages.

## 3️⃣ How are platforms implemented?

Each platform module has to be structured in the way that the model `platform` platform is structured.

### 📦 Platform Module

In order to allow for the easy extensibility of `d4v1d`, some standard functions have to be implemented:

#### `init`

> `init () -> Platform`

This method is called by the `d4v1d` platform loader upon discovering the platform module. It is used to **register the platform** with the `d4v1d` core, and allows for **custom initialization** of the platform.

It should return an instance of the [`Platform` class](#🚉-platform-class).

### 🚉 Platform class

> `d4v1d.platforms.platform.Platform`

Every platform **needs to extend this class**, and implement at least the following methods, since `d4v1d` makes use of them, to allow for some sort of **cross-platform data collection & analysis**:

#### `group`

> `group (self, name: str) -> d4v1d.platforms.platform.group.Group`

Create a new platform-specific group - i.e. a collection of bots for the platform that can be used to scrape new data.

#### `user`

> `user (self, username: str, refresh: bool = False, group: Optional[Group] = None) -> Info[User]`

Get generic information about a user of the social-media platform. 

Note that this returns info on a `User` object - you can, and probably should, of course use your own user classes with more platform-specific info, however, just make sure to inherit from `User` and fill all its required fields, since they represent info that should generally be available on **all** social-media platforms.

#### `users`

> `users (self) -> List[Info[User]]`

Get all locally cached users - i.e. users, whose information has been collected and locally stored in the past. 

Once again, the returned `User` objects should be instances of user classes that inherited from the `User` base class.

#### `cmds`

> `cmds: Dict[str, Union[Command, Dict[str, Any]]]`

It **isn't required** to override this attribute - use it only, if you want to add custom commands to your platform. Actually that isn't quite true, you should to override this, in order to at least provide access
to the `add bot` command, since that one can't really be provided by `d4v1d` as bots can be very platform specific and hard to generalize the creation of.

### 📊 Info Class

> `d4v1d.platforms.platform.info.Info`

This class is used to wrap the information that is retrieved from the platform. It contains the following attributes:

```md
- value (Any): The information
- date (datetime): The date of the information
- platform (Platform): The platform
```

This class has been introduced, because it seems rather reasonable to assume that the information retrieved from a platform is **not static**, but rather **changes over time**.

### 🧑 User Class

> `d4v1d.platforms.platform.user.User`

This class is the base class for all kinds of social-media users of all kinds of social-media platforms. 

Any new platforms should define own
user classes that extend this one and **always** contain values for at least the attributes defined in this class, as they're meant to be common across social-media platforms.

### 🤖 Bot Class

> `d4v1d.platforms.platform.bot.Bot`

This class is the "adapter" between `d4v1d` and the social-media platform. As you might have guessed, a *bot* represents an **automated user** - be it someone that's signed-in, or more preferably, if possible, someone that's just browsing anonymously.

Since the **core will never call** any methods of **this class directly**, it is not necessary to adhere to any specific naming convention for the methods of this class - just keep it clean and understandable I guess.

You can find examples for what the implementation of a bot could look like in the standard platforms that ship with `d4v1d` (i.e. [instagram](../platforms/instagram/), etc.).

### 👥 Group Class

> `d4v1d.platforms.platform.bot.Group`

Generally, in order to **avoid getting banned** and just to load balance in general, it seems reasonable to create groups of bots that can be used to **interact with the platform**. The idea being that not only one user does all the scraping, but the load is divided in order to make it less noticable.

Of course, groups can also just contain a single bot - however, it's always an option to add more.

Generally, I'd recommend, you never access instances of the `Bot` class directly, but only command and control as part of a group.

### 🗃️ Database Class

> `d4v1d.platforms.platform.db.Database`

It's up to you to decide what database format to use for your platform implementations. As long as you can provide the info that is required by the `d4v1d` core (as specified in the description of the [`Platform` class](#🚉-platform-class)), you can use whatever you want.

If you want, you can even let the user decide between multiple database formats and this is the reason as to why you should implement a general `Database` class - it'd probably be a good idea to go with the naming convention `<PLATFORM-NAME>Database`, e.g. `InstagramDatabase` - and extend it with the actual database implementations. For inspiration, you can take a look at how the standard platforms that ship with `d4v1d` are implemented (e.g. [instagram](../platforms/instagram/)).

### 🕹️ Commands Module

> `d4v1d.platforms.platform.cmd`

The commands module contains all the commands that are available for the platform. These commands are then used by the `d4v1d` core to grant the user access to them.

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
