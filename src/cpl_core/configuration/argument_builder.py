from typing import Union

from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum
from cpl_core.configuration.executable_argument import ExecutableArgument
from cpl_core.configuration.flag_argument import FlagArgument
from cpl_core.configuration.variable_argument import VariableArgument
from cpl_core.console import Console


class ArgumentBuilder:

    @staticmethod
    def build_argument(arg_type: ArgumentTypeEnum, *args, **kwargs) -> Union[
        ExecutableArgument, FlagArgument, VariableArgument]:
        argument = None
        try:
            match arg_type:
                case ArgumentTypeEnum.Flag:
                    argument = FlagArgument(*args, **kwargs)
                case ArgumentTypeEnum.Executable:
                    argument = ExecutableArgument(*args, **kwargs)
                case ArgumentTypeEnum.Variable:
                    argument = VariableArgument(*args, **kwargs)
                case _:
                    Console.error('Invalid argument type')
                    Console.close()
        except TypeError as e:
            Console.error(str(e))
            Console.close()
        return argument
