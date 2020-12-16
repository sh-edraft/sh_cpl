import os

from sh_edraft.cli.command.base.command_base import CommandBase
from sh_edraft.console.console import Console


class New(CommandBase):

    def __init__(self):
        CommandBase.__init__(self)

    def run(self, args: list[str]):
        rel_path = f'{os.path.dirname(__file__)}/../'
        if len(args) == 0:
            Console.error(f'Expected arguments {args}')
            Console.error('Run \'cpl help\'')
            return

        elif len(args) != 2:
            Console.error(f'Invalid arguments {args}')
            Console.error('Run \'cpl help\'')
            return

        if not os.path.isdir(f'{rel_path}/templates/{args[0]}'):
            Console.error(f'Unexpected argument {args[0]}')
            Console.error('Run \'cpl help\'')

        sub_args = args[1:]

        if len(sub_args) != 1:
            Console.error(f'Unexpected argument {sub_args[1]}')
            Console.error('Run \'cpl help\'')

        if not (sub_args[0].startswith('.') or sub_args[0].startswith('/')):
            full_path = f'./{sub_args[0]}'
        else:
            full_path = sub_args[0]

        name = os.path.basename(full_path)
        path = os.path.dirname(full_path)

        if args[0] in ['base', 'class', 'configmodel', 'enum', 'service']:
            if not os.path.isdir(path):
                os.makedirs(path)
        else:
            if not os.path.isdir(full_path):
                os.makedirs(full_path)

        for r, d, f in os.walk(f'{rel_path}/templates/{args[0]}'):
            for file in f:
                template_content = ''
                with open(f'{r}/{file}') as template:
                    template_content = template.read()
                    template.close()

                file = file.replace('txt', 'py')
                if args[0] in ['base', 'class', 'configmodel', 'enum', 'service']:
                    suffix = None

                    if args[0] == 'base':
                        suffix = 'base'

                    elif args[0] == 'configmodel':
                        suffix = 'settings'

                    elif args[0] == 'service':
                        suffix = 'service'

                    if suffix is not None:
                        file_path = f'{path}/{name}_{suffix}.py'
                    else:
                        file_path = f'{path}/{name}.py'
                else:
                    file_path = f'{full_path}/{file}'

                with open(file_path, 'w+') as pyfile:
                    if name[0].islower():
                        name = f'{name[0].upper()}{name[1:]}'

                    if args[0] == 'base':
                        template_content = template_content.replace('$Name', f'{name}Base')
                        pyfile.write(template_content)

                    elif args[0] == 'configmodel':
                        template_content = template_content.replace('$Name', f'{name}Settings')
                        pyfile.write(template_content)

                    elif args[0] == 'service':
                        template_content = template_content.replace('$Name', f'{name}Service')
                        template_content = template_content.replace('$Base', f'{name}Base')
                        pyfile.write(template_content)

                    else:
                        template_content = template_content.replace('$Name', name)
                        pyfile.write(template_content)

                    pyfile.close()
