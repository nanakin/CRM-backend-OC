"""The main file of the CRM application.

The CRM application is design for employees, customers, contracts and events management using a command-line interface.
Persistent data are stored in a remote or local database.

This file initialize Model-View-Controller components and execute the user command.
"""

import sentry_sdk
import toml

from controller import Controller
from model import Model
from view.cli import View  # change to dynamic import if multiple views


def log_record_setup() -> None:
    """Initialization of the error monitoring tool."""

    sentry_sdk.init(
        dsn="https://2d9b866802f9b43b93fa9a2ea2f3a8a2@o4506144422494208.ingest.sentry.io/4506144429309952",
        # Set traces_sample_rate to 1.0 to capture 100% for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        profiles_sample_rate=1.0,
    )


def main() -> None:
    """The main entry point of the CRM application."""

    # load application config file
    config = toml.load("crm.toml")

    # setup for exceptions record
    do_record = config["error_tracing"]["record"]
    if do_record:
        log_record_setup()

    # initialize Model-View-Controller components

    view = View()

    database_options = config["database"]
    do_fill_db = config["database"]["reset"] and config["database_sample"]["reset_with_sample"]

    model = Model(**database_options)
    if do_fill_db:  # testing purpose
        model.populate_with_sample()

    controller = Controller(view, model)

    # execute user command
    controller.read_and_execute_command()


if __name__ == "__main__":
    main()
