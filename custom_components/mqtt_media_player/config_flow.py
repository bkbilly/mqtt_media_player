import json

from homeassistant import config_entries
from homeassistant.helpers.service_info.mqtt import MqttServiceInfo

from .const import DOMAIN


@config_entries.HANDLERS.register(DOMAIN)
class MqttMediaPlayerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_mqtt(self, discovery_info=None):
        """Handle MQTT discovery.

        Two callers start this flow:
        - Home Assistant's MQTT integration, through the "mqtt" topics in
          manifest.json, with an MqttServiceInfo. This works even before the
          integration has any entry, so no configuration.yaml line is needed.
        - This integration's own subscription in async_setup (once it is set
          up), with a dict of name, discovery_topic and discovery_data.
        """
        if discovery_info is None:
            return self.async_abort(reason="no_discovery_info")

        if isinstance(discovery_info, MqttServiceInfo):
            topic = discovery_info.topic
            if not topic.endswith("/config"):
                return self.async_abort(reason="not_a_config_topic")

            payload = discovery_info.payload
            if isinstance(payload, (bytes, bytearray)):
                payload = payload.decode("utf-8", errors="replace")
            if not payload or not payload.strip():
                # An empty retained config means the device was removed.
                return self.async_abort(reason="empty_config")

            try:
                config_data = json.loads(payload)
            except json.JSONDecodeError:
                return self.async_abort(reason="invalid_discovery_info")

            # Same shape as the flows started from async_setup.
            discovery_info = {
                "name": topic.split("/")[-2],  # the part right before /config
                "discovery_topic": topic,
                "discovery_data": config_data,
            }

        device_name = discovery_info.get("name", "MQTT Media Player")

        # Check if already configured
        await self.async_set_unique_id(device_name)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=device_name,
            data=discovery_info
        )

    async def async_step_user(self, user_input=None):
        """Handle manual configuration attempts."""
        return self.async_abort(reason="mqtt_discovery_only")
