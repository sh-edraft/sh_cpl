import setuptools

setuptools.setup(
    name='sh_edraft',
    version='2020.0.1',
    packages=setuptools.find_packages(exclude=["tests*"]),
    url='https://www.sh-edraft.de',
    license='MIT',
    author='Sven Heidemann',
    author_email='edraft.sh@gmail.com',
    description='sh-edraft python common lib',
    python_requires='>=3.8',
    install_requires=[
        'discord.py',
        'flask',
        'mysql-connector',
        'SQLAlchemy',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'cpl = sh_edraft.cli.cpl_cli:CPLCli.main'
        ]
    }
)
