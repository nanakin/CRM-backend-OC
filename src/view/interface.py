"""Define the interface for all the views classes, these methods will be used by the controller."""
from abc import ABC, abstractmethod
from view.requests import FullRequest
from view.log import LogStatus


class IView(ABC):
    """A valid view must implements the following methods."""

    @abstractmethod
    def read_user_input(self) -> FullRequest | None:
        """Retrieve user command (request)."""

    @abstractmethod
    def notification(self, status: LogStatus, message: str) -> None:
        """Display a nice message."""

    @abstractmethod
    def ask_credentials(self) -> tuple[str, str]:
        """Ask employee credentials."""

    @abstractmethod
    def display_employees(self, data: list[dict]) -> None:
        """Display given employees."""

    @abstractmethod
    def display_employee(self, data: dict) -> None:
        """Display a given employee."""

    @abstractmethod
    def display_customers(self, data: list[dict]) -> None:
        """Display given customers."""

    @abstractmethod
    def display_customer(self, data: dict) -> None:
        """Display a given customer."""

    @abstractmethod
    def display_contracts(self, data: list[dict]) -> None:
        """Display given contracts."""

    @abstractmethod
    def display_contract(self, data: dict) -> None:
        """Display a given contract."""

    @abstractmethod
    def display_events(self, data: list[dict]) -> None:
        """Display given events."""

    @abstractmethod
    def display_event(self, data: dict) -> None:
        """Display a given event."""
