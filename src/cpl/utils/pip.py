import subprocess
import sys


class Pip:

    @staticmethod
    def get_package(package: str) -> str:
        result = subprocess.check_output([sys.executable, "-m", "pip", "show", package])

        new_package: list[str] = str(result, 'utf-8').lower().split('\n')
        new_version = ''

        for atr in new_package:
            if 'version' in atr:
                new_version = atr.split(': ')[1]

        return f'{package}=={new_version}'

    @staticmethod
    def install(package: str, *args, source: str = None, stdout=None, stderr=None):
        pip_args = [sys.executable, "-m", "pip", "install"]

        for arg in args:
            pip_args.append(arg)

        if source is not None:
            pip_args.append(f'--extra-index-url')
            pip_args.append(source)

        pip_args.append(package)
        subprocess.run(pip_args, stdout=stdout, stderr=stderr)
