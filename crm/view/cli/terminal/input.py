from rich.prompt import Prompt

from .console import console


def ask_credentials():
    console.print("This action requires user authentication")
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    return username, password
