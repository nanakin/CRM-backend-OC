from model import Model

from view import View
from controller import Controller
import toml


def main():
    # load config file
    config = toml.load("crm.toml")

    # initialize Model-View-Controller components
    view = View()
    data = Model(**config["database"])
    controller = Controller(view, data)

    # execute user command
    controller.read_and_execute_command()


if __name__ == "__main__":
    main()
