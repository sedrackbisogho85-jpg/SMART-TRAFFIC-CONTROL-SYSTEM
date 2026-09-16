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


