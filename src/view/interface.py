"""Define the interface for all the views classes, these methods will be used by the controller."""
from abc import ABC, abstractmethod


class IView(ABC):
    """A valid view must implements the following methods."""

    @abstractmethod
    def display_employees(self, data) -> None:
        """Display all employees from the database."""
