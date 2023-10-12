from model import Model

from view import View
from controller import Controller
import toml


def main():
    # load config file
    config = toml.load("crm.toml")

    # initialize Model-View-Controller components
    view = View()
    model = Model(**config["database"])
    if config["database"]["reset"] and config["database_sample"]["reset_with_sample"]:
        model.populate_with_sample()
    controller = Controller(view, model)

    # execute user command
    controller.read_and_execute_command()


if __name__ == "__main__":
    main()
