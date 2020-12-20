import setuptools

setuptools.setup(
    name='sh_edraft',
    version='2020.0.1',
    packages=setuptools.find_packages(exclude=["tests*"]),
    url='https://www.sh-edraft.de',
    license='MIT',
    author='Sven Heidemann',
    author_email='edraft.sh@gmail.com',
    include_package_data=True,
    description='sh-edraft python common lib',
    python_requires='>=3.8',
    install_requires=[
        'discord.py',
        'flask',
        'mysql-connector',
        'SQLAlchemy',
        'termcolor',
        'pyfiglet',
        'tabulate',
        'smtplib'
    ],
    entry_points={
        'console_scripts': [
            'cpl = sh_edraft.cli.cpl_cli.cli:main'
        ]
    }
)
