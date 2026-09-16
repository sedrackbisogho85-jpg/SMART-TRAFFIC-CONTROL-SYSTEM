#TRAFFIC CONTROL SYSTEM

from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, List, Optional, Type


# =============================================================================
# PERSON 1 – Classes & Objects (Foundation)
# Lecture note: We start by identifying the key “things” in the problem
# (traffic lights and a junction) and turn them into classes.
# =============================================================================

class Colour(Enum):
    """Allowed colours for a traffic light. Using an Enum prevents invalid values."""

    RED = "red"
    AMBER = "amber"
    GREEN = "green"

    def __str__(self) -> str:
        return self.name.capitalize()


class InvalidColourError(Exception):
    """Raised when code tries to use a colour that is not RED/AMBER/GREEN."""


class LightNotFoundError(Exception):
    """Raised when a requested light does not exist in the junction."""


class JunctionError(Exception):
    """General problem with a junction operation."""


class TrafficLight:
    """A single software-controlled traffic light."""

    _CYCLE = (Colour.RED, Colour.GREEN, Colour.AMBER)

    def __init__(self, location: str, initial_colour: Colour = Colour.RED):
        if not isinstance(location, str) or not location.strip():
            raise ValueError("Location must be a non-empty string.")
        if not isinstance(initial_colour, Colour):
            raise InvalidColourError(
                f"'{initial_colour}' is not a valid Colour. "
                f"Allowed values: {[c.name for c in Colour]}"
            )

        self._location = location.strip()
        self._colour = initial_colour

    @property
    def location(self) -> str:
        """Read-only access to the light's location."""
        return self._location

    @property
    def colour(self) -> Colour:
        """Read-only access to the current colour."""
        return self._colour

    def advance(self) -> None:
        """Move to the next colour in the fixed cycle."""
        idx = self._CYCLE.index(self._colour)
        self._colour = self._CYCLE[(idx + 1) % len(self._CYCLE)]

    def set_colour(self, new_colour: Colour) -> None:
        """Force the light to a valid colour."""
        if not isinstance(new_colour, Colour):
            raise InvalidColourError(
                f"'{new_colour}' is not a valid Colour. "
                f"Allowed values: {[c.name for c in Colour]}"
            )
        self._colour = new_colour

    def is_stop(self) -> bool:
        """Return True if the light currently means stop."""
        return self._colour in (Colour.RED, Colour.AMBER)

    def describe(self) -> str:
        """Human-readable description for road users and operators."""
        status = "STOP" if self.is_stop() else "GO"
        return f"{self._location} is {self._colour} ({status})"

    def __str__(self) -> str:
        return self.describe()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(location={self.location!r}, colour={self.colour!s})"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this light into a JSON-safe dictionary.

        Note: we save the Enum value ("red") instead of the name ("RED") so the
        payload is simply JSON-friendly data and matches the current codebase.
        """
        return {
            "type": self.__class__.__name__,
            "location": self.location,
            "colour": self.colour.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrafficLight":
        """Create a light from a serialized dictionary.

        This resolves the class, then delegates to that class's constructor.
        Subclasses override _construct() so the extra subclass state is restored.
        """
        if not isinstance(data, dict):
            raise JunctionError("Light data must be a dictionary.")

        try:
            location = data["location"]
            colour = Colour(data["colour"])
        except InvalidColourError:
            raise
        except (KeyError, TypeError, ValueError) as exc:
            raise JunctionError(f"Invalid light payload: {data!r}") from exc

        light_class = _resolve_light_class(data.get("type", cls.__name__))
        if light_class is not cls:
            return light_class.from_dict(data)
        return cls._construct(location, colour, data)

    @classmethod
    def _construct(cls, location: str, colour: Colour, data: Dict[str, Any]) -> "TrafficLight":
        return cls(location, colour)

