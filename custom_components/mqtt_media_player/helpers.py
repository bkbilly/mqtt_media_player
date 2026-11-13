from homeassistant.config_entries import ConfigEntry


def topic_device_id(topic: str) -> str:
    """Return the device ID for a discovery config topic.

    homeassistant/media_player/<object_id>/config -> <object_id>
    homeassistant/media_player/<node_id>/<object_id>/config -> <node_id>/<object_id>

    The node ID is part of the device ID, as in Home Assistant's own MQTT
    discovery: publishers on several machines can use the same object ID, each
    under its own node ID (e.g. the host name).
    """
    return "/".join(topic.split("/")[2:-1])


def entry_device_id(entry: ConfigEntry) -> str:
    """Return the device ID (see topic_device_id) for an entry.

    The entry title starts out as the device ID but can be renamed in the UI, so it
    must not be used to identify the device. The unique ID and data["name"] are set
    to the device ID when the entry is created and change only in a
    migration (migration.py).
    """
    return entry.unique_id or entry.data.get("name") or entry.title
