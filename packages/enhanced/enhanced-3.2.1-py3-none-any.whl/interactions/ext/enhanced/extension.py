import types
from hashlib import md5
from inspect import getmembers, iscoroutinefunction
from logging import Logger
from re import fullmatch
from typing import List, Optional, Union

from interactions import MISSING, Client, CommandContext, ComponentContext, Extension, Guild
from interactions.ext import Base, Version, VersionAuthor

from ._logging import get_logger

log: Logger = get_logger("extension")


class VersionAuthorPatch(VersionAuthor):
    def __init__(self, name, *, shared=False, active=True, email=None) -> None:
        self.name = name
        self._co_author = shared
        self.active = active
        self.email = email
        self._hash = md5(self.__str__().encode("utf-8"))


class VersionPatch(Version):
    __slots__ = ("_authors",)


class BasePatch(Base):
    __slots__ = ("long_description",)


version = (
    VersionPatch(
        version="3.2.1",
        author=VersionAuthorPatch(
            name="Toricane",
            email="prjwl028@gmail.com",
        ),
    ),
)
base = BasePatch(
    name="enhanced",
    version=version,
    description="Enhanced interactions for interactions.py",
    link="https://github.com/interactions-py/enhanced",
    packages=["interactions.ext.enhanced"],
    requirements=[
        "discord-py-interactions>=4.1.0",
        "typing_extensions",
    ],
)


def sync_subcommands(self, client):
    """Syncs the subcommands in the extension."""
    if not any(
        hasattr(func, "__subcommand__")
        for _, func in getmembers(self, predicate=iscoroutinefunction)
    ):
        return
    bases = {
        func.__base__: func.__data__
        for _, func in getmembers(self, predicate=iscoroutinefunction)
        if hasattr(func, "__subcommand__")
    }
    commands = []

    for base, subcommand in bases.items():
        subcommand.set_self(self)
        client.event(subcommand.inner, name=f"command_{base}")
        commands.extend(subcommand.raw_commands)

    if client._automate_sync:
        if client._loop.is_running():
            [client._loop.create_task(client._synchronize(command)) for command in commands]
        else:
            [client._loop.run_until_complete(client._synchronize(command)) for command in commands]
    for subcommand in bases.values():
        scope = subcommand.scope
        if scope is not MISSING:
            if isinstance(scope, list):
                [client._scopes.add(_ if isinstance(_, int) else _.id) for _ in scope]
            else:
                client._scopes.add(scope if isinstance(scope, int) else scope.id)


class EnhancedExtension(Extension):
    """
    Enables modified external commands, subcommands, callbacks, and more.

    Use this class instead of `Extension` when using extensions.

    ```py
    # extension.py
    from interactions.ext.enhanced import EnhancedExtension

    class Example(EnhancedExtension):
        ...

    def setup(client):
        Example(client)
    ```
    """

    def __new__(cls, client: Client, *args, **kwargs):
        for func in getmembers(cls, predicate=iscoroutinefunction):
            if hasattr(func, "__command_data__"):
                scope = func.__command_data__[1].get("scope", MISSING)
                debug_scope = func.__command_data__[1].get("debug_scope", True)
                del func.__command_data__[1]["debug_scope"]
                if scope is MISSING and debug_scope and hasattr(client, "__debug_scope"):
                    func.__command_data__[1]["scope"] = client.__debug_scope

        log.debug("Syncing subcommands...")
        sync_subcommands(cls, client)
        log.debug("Synced subcommands")

        self = super().__new__(cls, client, *args, **kwargs)
        return self


class Enhanced(Extension):
    """
    This is the core of this library, initialized when loading the extension.

    It applies hooks to the client for additional and modified features.

    ```py
    # main.py
    client.load("interactions.ext.enhanced", ...)  # optional args/kwargs
    ```

    Parameters:

    * `(?)client: Client`: The client instance. Not required if using `client.load("interactions.ext.enhanced", ...)`.
    * `?debug_scope: int | Guild | list[int] | list[Guild]`: The debug scope to apply to global commands.
    * `?add_subcommand: bool`: Whether to add subcommand hooks to the client. Defaults to `True`.
    * `?modify_callbacks: bool`: Whether to modify callback decorators. Defaults to `True`.
    * `?modify_command: bool`: Whether to modify the command decorator. Defaults to `True`.
    """

    def __init__(
        self,
        bot: Client,
        debug_scope: Optional[Union[int, Guild, List[int], List[Guild]]] = None,
        add_subcommand: Optional[bool] = True,
        modify_callbacks: Optional[bool] = True,
        modify_command: Optional[bool] = True,
    ):
        if not isinstance(bot, Client):
            log.critical("The bot must be an instance of Client")
            raise TypeError(f"{bot.__class__.__name__} is not interactions.Client!")
        log.debug("The bot is an instance of Client")

        if debug_scope is not None:
            log.debug("Setting debug_scope (debug_scope)")
            setattr(bot, "__debug_scope", debug_scope)

        if add_subcommand:
            from .subcommands import subcommand_base

            log.debug("Adding bot.subcommand_base (add_subcommand)")
            bot.subcommand_base = types.MethodType(subcommand_base, bot)

        if modify_callbacks:
            from .callbacks import component, modal

            log.debug("Modifying component callbacks (modify_callbacks)")
            bot.component = types.MethodType(component, bot)

            bot.event(self._on_component, "on_component")
            log.debug("Registered on_component")

            log.debug("Modifying modal callbacks (modify_callbacks)")
            bot.modal = types.MethodType(modal, bot)

            bot.event(self._on_modal, "on_modal")
            log.debug("Registered on_modal")

        if modify_command:
            from .commands import command

            log.debug("Modifying bot.command (modify_command)")
            bot.old_command = bot.command
            bot.command = types.MethodType(command, bot)

        log.info("Hooks applied")

    async def _on_component(self, ctx: ComponentContext):
        """on_component callback for modified callbacks."""
        websocket = self.client._websocket
        if any(
            any(hasattr(func, "startswith") or hasattr(func, "regex") for func in funcs)
            for _, funcs in websocket._dispatch.events.items()
        ):
            for decorator_custom_id, funcs in websocket._dispatch.events.items():
                for func in funcs:
                    if hasattr(func, "startswith"):
                        if ctx.data.custom_id.startswith(
                            decorator_custom_id.replace("component_startswith_", "")
                        ):
                            log.info(f"{func} startswith {func.startswith} matched")
                            return websocket._dispatch.dispatch(decorator_custom_id, ctx)
                    elif hasattr(func, "regex") and fullmatch(
                        func.regex,
                        ctx.data.custom_id.replace("component_regex_", ""),
                    ):
                        log.info(f"{func} regex {func.regex} matched")
                        return websocket._dispatch.dispatch(decorator_custom_id, ctx)

    async def _on_modal(self, ctx: CommandContext):
        """on_modal callback for modified callbacks."""
        websocket = self.client._websocket
        if any(
            any(hasattr(func, "startswith") or hasattr(func, "regex") for func in funcs)
            for _, funcs in websocket._dispatch.events.items()
        ):
            for decorator_custom_id, funcs in websocket._dispatch.events.items():
                for func in funcs:
                    if hasattr(func, "startswith"):
                        if ctx.data.custom_id.startswith(
                            decorator_custom_id.replace("modal_startswith_", "")
                        ):
                            log.info(f"{func} startswith {func.startswith} matched")
                            return websocket._dispatch.dispatch(decorator_custom_id, ctx)
                    elif hasattr(func, "regex") and fullmatch(
                        func.regex,
                        ctx.data.custom_id.replace("modal_regex_", ""),
                    ):
                        log.info(f"{func} regex {func.regex} matched")
                        return websocket._dispatch.dispatch(decorator_custom_id, ctx)


def setup(
    bot: Client,
    add_subcommand: Optional[bool] = True,
    modify_callbacks: Optional[bool] = True,
    modify_command: Optional[bool] = True,
    debug_scope: Optional[Union[int, Guild, List[int], List[Guild]]] = None,
) -> None:
    """
    This function initializes the core of the library, `Enhanced`.

    It applies hooks to the client for additional and modified features.

    ```py
    # main.py
    client.load("interactions.ext.enhanced", ...)  # optional args/kwargs
    ```

    Parameters:

    * `(?)client: Client`: The client instance. Not required if using `client.load("interactions.ext.enhanced", ...)`.
    * `?debug_scope: int | Guild | list[int] | list[Guild]`: The debug scope to apply to global commands.
    * `?add_subcommand: bool`: Whether to add subcommand hooks to the client. Defaults to `True`.
    * `?modify_callbacks: bool`: Whether to modify callback decorators. Defaults to `True`.
    * `?modify_command: bool`: Whether to modify the command decorator. Defaults to `True`.
    """
    log.info("Setting up Enhanced")
    return Enhanced(bot, debug_scope, add_subcommand, modify_callbacks, modify_command)
