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


# =============================================================================
# PERSON 3 - Colour changes
# Implements the required red -> green -> amber -> red cycle.
# =============================================================================

    def advance(self) -> None:
        """Move red to green, green to amber, or amber to red."""
        current_index = self._CYCLE.index(self.colour)
        next_index = (current_index + 1) % len(self._CYCLE)
        self._colour = self._CYCLE[next_index]


# =============================================================================
# PERSON 4 - Stop status and descriptions
# Tells road users whether the light means STOP and describes its state.
# =============================================================================

    def is_stop(self) -> bool:
        """Return whether this light currently means stop."""
        return self.colour in (Colour.RED, Colour.AMBER)

    def describe(self) -> str:
        """Return the light's location, colour, and traffic instruction."""
        instruction = "STOP" if self.is_stop() else "GO"
        return f"{self.location}: {self.colour} ({instruction})"


# =============================================================================
# PERSON 5 - Multiple lights
# Displays the states of at least two TrafficLight objects.
# =============================================================================

def print_lights(lights: list[TrafficLight]) -> None:
    for light in lights:
        print(light.describe())


# =============================================================================
# PERSON 6 - Invalid-colour demonstration
# Attempts an invalid colour and shows that the program refuses it.
# =============================================================================


if __name__ == "__main__":
    main_gate = TrafficLight("Main Gate / Chapel Road")
    library = TrafficLight("Library / Science Road", Colour.GREEN)
    lights = [main_gate, library]

    print("Initial states:")
    print_lights(lights)

    print("\nAfter advancing through the cycle:")
    for _ in range(3):
        for light in lights:
            light.advance()
        print_lights(lights)

    print("\nAutomatic invalid-colour check:")
    try:
        main_gate.set_colour("blue")
    except InvalidColourError as error:
        print(f"Rejected: {error}")