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
        # Find where the current colour sits in the defined cycle sequence.
        # For example, if self.colour is "green" and _CYCLE is ["red", "green", "amber"],
        # this returns 1 (the index of "green").
        current_index = self._CYCLE.index(self.colour)
        
        # Work out the index of the next colour in the cycle.
        # Adding 1 moves us forward by one position.
        # The len(self._CYCLE) wraps the index back to 0
        # when we reach the end, so "amber" loops back to "red" automatically.
        next_index = (current_index + 1) % len(self._CYCLE)
        
        # Update the traffic light's colour to the next one in the sequence.
        # This is the only state change in the method — everything else is
        # just calculation to determine what that new colour should be.
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


