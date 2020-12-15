import os


class CLICommands:

    @classmethod
    def new(cls, args: list[str]):
        if not os.path.isdir(f'./templates/{args[0]}'):
            cls.unexpected_command(args[0])

        sub_args = args[1:]

        if len(sub_args) != 1:
            cls.unexpected_argument(sub_args[1])

        full_path = sub_args[0]
        name = os.path.basename(full_path)
        path = os.path.dirname(full_path)

        if args[0] in ['base', 'class', 'configmodel', 'enum', 'service']:
            if not os.path.isdir(path):
                os.makedirs(path)
        else:
            if not os.path.isdir(full_path):
                os.makedirs(full_path)

        for r, d, f in os.walk(f'./templates/{args[0]}'):
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

                    if args[0] == 'configmodel':
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

    @staticmethod
    def help():
        print('Commands:')

    @classmethod
    def unexpected_command(cls, command: str):
        print(f'Unexpected command {command}')
        cls.help()
        exit()

    @classmethod
    def unexpected_argument(cls, argument: str):
        print(f'Unexpected argument {argument}')
        cls.help()
        exit()
