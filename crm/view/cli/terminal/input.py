from rich.prompt import Prompt

from crm.view.common import ViewOperationFailed

from .console import console


def ask_credentials():
    console.print("ℹ️  This action requires user authentication")
    try:
        username = Prompt.ask("Username")
        password = Prompt.ask("Password", password=True)
        return username, password
    except KeyboardInterrupt:
        raise ViewOperationFailed("Authentication cancelled.")
