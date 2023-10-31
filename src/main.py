import toml

from controller import Controller
from model import Model
from view import View
import sentry_sdk


def sentry_setup():
    sentry_sdk.init(
        dsn="https://2d9b866802f9b43b93fa9a2ea2f3a8a2@o4506144422494208.ingest.sentry.io/4506144429309952",
        # Set traces_sample_rate to 1.0 to capture 100% for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        profiles_sample_rate=1.0,
    )


def main():

    # keep errors log
    sentry_setup()

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
