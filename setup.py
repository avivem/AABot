from setuptools import setup

setup(
    name='AABot',
    version='1.0',
    description='A simple Discord bot written in Python using the Discord.py API',
    author='Aviv Elazar-Mittelman',
    author_email='avivelazarmittelman@gmail.com',
    packages=['AABot'],
    install_requires=['discord.py','python-dotenv']
)