from typing import Type, Optional

from cpl_core.configuration.runnable_argument_abc import RunnableArgumentABC


class ConsoleArgument:

    def __init__(self,
                 token: str,
                 name: str,
                 aliases: list[str],
                 value_token: str,
                 is_value_token_optional: bool = None,
                 runnable: Type[RunnableArgumentABC] = None,
                 console_arguments: list['ConsoleArgument'] = None
                 ):
        r"""Representation of an console argument

        Parameter
        ---------
            token: :class:`str`
            name: :class:`str`
            aliases: list[:class:`str`]
            value_token: :class:`str`
            is_value_token_optional: :class:`bool`
            runnable: :class:`cpl_core.configuration.console_argument.ConsoleArgument`
            console_arguments: List[:class:`cpl_core.configuration.console_argument.ConsoleArgument`]
        """
        self._token = token
        self._name = name
        self._aliases = aliases
        self._value_token = value_token
        self._is_value_token_optional = is_value_token_optional
        self._console_arguments = console_arguments if console_arguments is not None else []
        self._runnable_type = runnable
        self._runnable: Optional[RunnableArgumentABC] = None

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
    def value_token(self) -> str:
        return self._value_token

    @property
    def is_value_token_optional(self) -> bool:
        return self._is_value_token_optional

    @property
    def console_arguments(self) -> list['ConsoleArgument']:
        return self._console_arguments

    @property
    def runnable_type(self) -> Type[RunnableArgumentABC]:
        return self._runnable_type

    def set_runnable(self, runnable: RunnableArgumentABC):
        self._runnable = runnable

    def add_console_argument(self, token: str, name: str, aliases: list[str], value_token: str,
                             is_value_token_optional: bool = None) -> 'ConsoleArgument':
        r"""Creates and adds a console argument to known console arguments

        Parameter
        ---------
            token: :class:`str`
                Specifies optional beginning of argument
            name :class:`str`
                Specifies name of argument
            aliases list[:class:`str`]
                Specifies possible aliases of name
            value_token :class:`str`
                Specifies were the value begins
            is_value_token_optional :class:`bool`
                Specifies if values are optional

        Returns
        ------
            self :class:`cpl_core.configuration.console_argument.ConsoleArgument` not created argument!
        """
        argument = ConsoleArgument(token, name, aliases, value_token, is_value_token_optional)
        self._console_arguments.append(argument)
        return self

    def run(self, args: list[str]):
        r"""Executes runnable if exists
        """
        if self._runnable is None:
            return
        self._runnable.run(args)
