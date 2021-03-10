class Template:

    @staticmethod
    def build_template_string(string: str) -> str:
        return_value = ''
        for i in range(0, len(string.splitlines())):
            line = string.splitlines()[i]
            if i == len(string.splitlines())-1:
                return_value += f'{line.strip()}'
                break

            return_value += f'{line.strip()}\n'

        return return_value
