"""Smart Junction – Software-Controlled Traffic Light System.

This file is organised to mirror the six-person assignment structure:
Person 1: classes and objects
Person 2: encapsulation
Person 3: relationships
Person 4: inheritance
Person 5: polymorphism
Person 6: exceptions and persistence
"""

from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, List, Optional


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


# =============================================================================
# PERSON 2 – Encapsulation
# Lecture note: We hide the internal data (_location, _colour, _lights)
# and only allow controlled access through properties and methods.
# This protects the integrity of each object.
# =============================================================================

# TrafficLight:
#   - _location and _colour are private
#   - location and colour are exposed as read-only properties
#   - colour can only be changed via advance() or set_colour()
#
# Junction:
#   - _lights is private
#   - external code should not mutate the list directly
#
# In the implementation below, this is handled through proper validation.


# =============================================================================
# PERSON 3 – Relationships
# Lecture note: A Junction “has-a” collection of TrafficLight objects
# (composition). We now add methods that express this relationship.
# =============================================================================

class Junction:
    """A named collection of traffic lights that belong together."""

    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Junction name must be a non-empty string.")
        self.name = name.strip()
        self._lights: List[TrafficLight] = []

    def add_light(self, light: TrafficLight) -> None:
        """Add a light to this junction."""
        if not isinstance(light, TrafficLight):
            raise TypeError("Only TrafficLight instances can be added to a junction.")
        self._lights.append(light)

    def remove_light(self, location: str) -> None:
        """Remove a light by its location."""
        for i, light in enumerate(self._lights):
            if light.location == location:
                del self._lights[i]
                return
        raise LightNotFoundError(f"No light found at '{location}'")

    def find_light(self, location: str) -> Optional[TrafficLight]:
        """Return the light at the given location, or None."""
        for light in self._lights:
            if light.location == location:
                return light
        return None

    def stop_count(self) -> int:
        """How many lights in this junction currently mean stop?"""
        return sum(1 for light in self._lights if light.is_stop())

    def advance_all(self) -> None:
        """Advance every light in the junction by one step."""
        for light in self._lights:
            light.advance()

    def lights(self) -> List[TrafficLight]:
        """Return a copy of the lights (encapsulation)."""
        return list(self._lights)

    def status_report(self) -> str:
        """Return a readable report of the junction state."""
        if not self._lights:
            return f"=== {self.name} ===\n  No traffic lights configured."

        lines = [f"=== {self.name} ==="]
        for light in self._lights:
            lines.append(f"  • {light.describe()}")
        return "\n".join(lines)


# =============================================================================
# PERSON 4 – Inheritance
# Lecture note: We create specialised kinds of traffic light that inherit
# all the common behaviour and then add or change only what is different.
# =============================================================================

class PedestrianLight(TrafficLight):
    """A traffic light that also controls a pedestrian crossing."""

    def describe(self) -> str:
        base = super().describe()
        walk = "WALK" if self.colour == Colour.GREEN else "DON'T WALK"
        return f"{base} | Pedestrian: {walk}"


class EmergencyLight(TrafficLight):
    """A light that can be forced into a permanent red state."""

    def __init__(self, location: str, initial_colour: Colour = Colour.RED):
        super().__init__(location, initial_colour)
        self._emergency_mode = False

    def activate_emergency(self) -> None:
        """Force the light to red and lock it."""
        self._emergency_mode = True
        self._colour = Colour.RED

    def deactivate_emergency(self) -> None:
        """Return to normal cycling behaviour."""
        self._emergency_mode = False

    def advance(self) -> None:
        """Emergency lights do not cycle while in emergency mode."""
        if not self._emergency_mode:
            super().advance()

    def describe(self) -> str:
        base = super().describe()
        if self._emergency_mode:
            return f"{base} [EMERGENCY MODE]"
        return base


# =============================================================================
# PERSON 5 – Polymorphism
# Lecture note: Because every light (normal, pedestrian, emergency) is a
# TrafficLight, a Junction can treat them all the same way.
# The correct version of advance() / describe() is chosen at run time.
# =============================================================================

# The same junction methods work with different subclasses.
# Each subclass overrides describe() and advance() without changing the API.


# =============================================================================
# PERSON 6 – Exceptions & Persistence
# Lecture note:
#   • Custom exceptions make error handling clear and specific.
#   • Persistence lets us save the whole junction state and restore it later.
# =============================================================================

class InvalidColourError(ValueError):
    """Raised when code tries to set a colour that is not RED/AMBER/GREEN."""
    pass


class LightNotFoundError(Exception):
    """Raised when a requested light does not exist in the junction."""
    pass


class JunctionError(Exception):
    """General problem with a junction operation."""
    pass


def _light_to_dict(light: TrafficLight) -> Dict[str, Any]:
    """Convert a light (any subclass) into a JSON-serialisable dictionary."""
    data = {
        "type": light.__class__.__name__,
        "location": light.location,
        "colour": light.colour.name,
    }
    if isinstance(light, EmergencyLight):
        data["emergency_mode"] = light._emergency_mode
    return data


def _light_from_dict(data: Dict[str, Any]) -> TrafficLight:
    """Recreate a light of the correct subclass from a dictionary."""
    colour = Colour[data["colour"]]
    location = data["location"]
    cls_name = data["type"]

    if cls_name == "PedestrianLight":
        light = PedestrianLight(location, colour)
    elif cls_name == "EmergencyLight":
        light = EmergencyLight(location, colour)
        if data.get("emergency_mode"):
            light.activate_emergency()
    else:
        light = TrafficLight(location, colour)
    return light


# Add persistence behaviour to the same Junction class.
def _save_junction(junction: "Junction", filename: str) -> None:
    """Save the whole junction state to a JSON file."""
    data = {
        "name": junction.name,
        "lights": [_light_to_dict(light) for light in junction._lights],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Junction saved to {filename}")


@classmethod
def _load_junction(cls, filename: str) -> "Junction":
    """Load a junction and all its lights from a JSON file."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    junction = cls(data["name"])
    for light_data in data["lights"]:
        junction.add_light(_light_from_dict(light_data))
    print(f"Junction loaded from {filename}")
    return junction


Junction.save = _save_junction
Junction.load = _load_junction


# =============================================================================
# DEMONSTRATION – Full system in action
# This section is used both for marking and for live lecture demos.
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SMART JUNCTION – FULL DEMONSTRATION")
    print("=" * 60)

    campus = Junction("Main Campus Junction")

    gate = TrafficLight("Main Gate / Chapel Road")
    library = TrafficLight("Library / Science Road")
    campus.add_light(gate)
    campus.add_light(library)

    print("\n1. Initial state (both lights start RED):")
    print(campus.status_report())

    print("\n2. Advancing lights and using relationship methods:")
    gate.advance()
    library.advance()
    library.advance()
    print(campus.status_report())
    print(f"Lights currently showing STOP: {campus.stop_count()}")

    print("\n3. Adding specialised lights (Inheritance):")
    pedestrian = PedestrianLight("Library Crossing")
    emergency = EmergencyLight("Hospital Approach")
    campus.add_light(pedestrian)
    campus.add_light(emergency)
    print(campus.status_report())

    print("\n4. Polymorphism – treating all lights the same way:")
    print("Advancing EVERY light (each type responds differently):")
    campus.advance_all()
    print(campus.status_report())

    print("\nActivating emergency mode on the emergency light:")
    emergency.activate_emergency()
    print(campus.status_report())

    print("\n5. Exception handling:")
    try:
        gate.set_colour("BLUE")
    except InvalidColourError as e:
        print(f"  Caught InvalidColourError: {e}")

    try:
        campus.remove_light("Non-existent Road")
    except LightNotFoundError as e:
        print(f"  Caught LightNotFoundError: {e}")

    print("\n6. Persistence (save / load):")
    campus.save("campus_junction.json")
    gate.advance()
    print("\nState AFTER saving and then changing a light:")
    print(campus.status_report())

    restored = Junction.load("campus_junction.json")
    print("\nRestored junction (should match the state at the moment of saving):")
    print(restored.status_report())

    print("\n" + "=" * 60)
    print("Demonstration complete.")
    print("=" * 60)