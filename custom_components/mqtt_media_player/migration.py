"""Config entry migration steps, called from async_migrate_entry."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .helpers import entry_device_id, topic_device_id

_LOGGER = logging.getLogger(__name__)


@callback
def migrate_to_1_2(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Include the node ID of the discovery topic in the device ID.

    Entries discovered before were keyed on the object ID alone (see
    topic_device_id), so a second publisher with the same object ID under
    another node ID was taken for the first one; they move to the new device ID.
    Entries added by hand, before discovery, get the discovery topic they were
    made for.

    The entity keeps its entity ID and history and only gets the new unique ID.
    It is keyed on the old device ID, or on the entry title if it was created
    before the device ID was used (renaming the entry then created a new entity).
    Only an entity of this entry is moved: the title can also be the device ID of
    another entry.
    """
    old_id = entry_device_id(entry)
    topic = entry.data.get("discovery_topic") or f"homeassistant/media_player/{old_id}/config"
    new_id = topic_device_id(topic)

    registry = er.async_get(hass)
    if not registry.async_get_entity_id("media_player", DOMAIN, new_id):
        for key in (old_id, entry.title):
            entity_id = registry.async_get_entity_id("media_player", DOMAIN, key)
            if entity_id and registry.async_get(entity_id).config_entry_id == entry.entry_id:
                registry.async_update_entity(entity_id, new_unique_id=new_id)
                _LOGGER.info("Migrated media player %s (%s) to device ID %s", entity_id, key, new_id)
                break
    hass.config_entries.async_update_entry(
        entry,
        data={**entry.data, "name": new_id, "discovery_topic": topic},
        unique_id=new_id,
        minor_version=2,
    )
