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


# =============================================================================
# PERSON 2 - Named locations
# Stores each light at a required, non-empty named location.
# =============================================================================

    @property
    def colour(self) -> Colour:
        return self._colour

    def set_colour(self, colour: Colour | str) -> None:
        """Set a valid colour, ignoring letter case and surrounding spaces."""
        if isinstance(colour, str):
            try:
                colour = Colour(colour.strip().lower())
            except ValueError as error:
                raise InvalidColourError(
                    f"Invalid colour: {colour!r}. Choose RED, AMBER, or GREEN."
                ) from error
        elif not isinstance(colour, Colour):
            raise InvalidColourError(
                f"Invalid colour: {colour!r}. Choose RED, AMBER, or GREEN."
            )

        self._colour = colour


