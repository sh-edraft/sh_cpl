from abc import ABC, abstractmethod

from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum


class ArgumentABC(ABC):
    @abstractmethod
    def __init__(
        self,
        token: str,
        name: str,
        aliases: list[str],
        prevent_next_executable: bool = False,
        console_arguments: list["ArgumentABC"] = None,
    ):
        r"""Representation of an console argument

        Parameter:
            token: :class:`str`
            name: :class:`str`
            aliases: list[:class:`str`]
            console_arguments: List[:class:`cpl_core.configuration.console_argument.ConsoleArgument`]
        """
        self._token = token
        self._name = name
        self._aliases = aliases
        self._prevent_next_executable = prevent_next_executable
        self._console_arguments = console_arguments if console_arguments is not None else []

    @property
    def token(self) -> str:
        return self._token

    @property
    def name(self) -> str:
        return self._name

    @property
    def aliases(self) -> list[str]:
        return self._aliases

    @property
    def prevent_next_executable(self) -> bool:
        return self._prevent_next_executable

    @property
    def console_arguments(self) -> list["ArgumentABC"]:
        return self._console_arguments

    def add_console_argument(self, arg_type: ArgumentTypeEnum, *args, **kwargs) -> "ArgumentABC":
        r"""Creates and adds a console argument to known console arguments

        Parameter:
            arg_type: :class:`str`
                Specifies the specific type of the argument

        Returns:
            self :class:`cpl_core.configuration.console_argument.ConsoleArgument` not created argument!
        """
        from cpl_core.configuration.argument_builder import ArgumentBuilder

        argument = ArgumentBuilder.build_argument(arg_type, *args, *kwargs)
        self._console_arguments.append(argument)
        return self
