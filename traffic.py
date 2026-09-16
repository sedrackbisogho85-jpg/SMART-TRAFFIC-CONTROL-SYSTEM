"""Simple software-controlled traffic lights for a campus junction."""

from enum import Enum


# =============================================================================
# PERSON 1 - Classes and colours
# Defines the allowed colours and the basic TrafficLight object.
# =============================================================================

class Colour(Enum):
    RED = "red"
    AMBER = "amber"
    GREEN = "green"

    def __str__(self) -> str:
        return self.value


class InvalidColourError(ValueError):
    """Raised when a traffic light is given an invalid colour."""


class TrafficLight:
    """A traffic light installed at a named location."""

    _CYCLE = (Colour.RED, Colour.GREEN, Colour.AMBER)

    def __init__(self, location: str, colour: Colour = Colour.RED):
        if not isinstance(location, str) or not location.strip():
            raise ValueError("Location must be a non-empty string.")

        self._location = location.strip()
        self.set_colour(colour)

    @property
    def location(self) -> str:
        return self._location


