import setuptools

setuptools.setup(
    name='sh_edraft_unittests',
    version='2020.0.1',
    packages=setuptools.find_packages(exclude=["tests*"]),
    url='https://www.sh-edraft.de',
    license='MIT',
    author='Sven Heidemann',
    author_email='edraft.sh@gmail.com',
    include_package_data=True,
    description='sh-edraft python common lib unittest',
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
    ]
)
