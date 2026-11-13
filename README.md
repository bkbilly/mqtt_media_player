# MQTT Media Player

Easiest way to add a custom MQTT Media Player with full auto-discovery support.

## Features

- 🔍 **MQTT Auto-Discovery** - Devices automatically appear in Home Assistant
- 🎵 **Full Media Control** - Play, pause, skip, volume, and more
- 🖼️ **Album Art Support** - Display cover art from MQTT
- 📊 **Progress Tracking** - Track position and duration
- 🔌 **Availability Monitoring** - Know when devices are online/offline
- 📁 **Media Browser** - Browse and play media from Home Assistant

## Installation
Easiest install is via [HACS](https://hacs.xyz/):

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bkbilly&repository=mqtt_media_player&category=integration)

## Configuration

### MQTT Discovery Message

Publish a JSON configuration message to `homeassistant/media_player/{object_id}/config`, or
`homeassistant/media_player/{node_id}/{object_id}/config` as in Home Assistant's
[MQTT discovery](https://www.home-assistant.io/integrations/mqtt/#discovery-topic). The node ID is part of the
device ID, so several publishers can use the same object ID under their own node ID (e.g. one per computer).

```json
{
  "name": "My Custom Player",
  "availability": {
    "topic": "myplayer/available",
    "payload_available": "online",
    "payload_not_available": "offline"
  },
  "state_state_topic": "myplayer/state",
  "state_title_topic": "myplayer/title",
  "state_artist_topic": "myplayer/artist",
  "state_album_topic": "myplayer/album",
  "state_duration_topic": "myplayer/duration",
  "state_position_topic": "myplayer/position",
  "state_volume_topic": "myplayer/volume",
  "state_mute_topic": "myplayer/mute",
  "state_albumart_topic": "myplayer/albumart",
  "state_mediatype_topic": "myplayer/mediatype",
  "command_volume_topic": "myplayer/set_volume",
  "command_mute_topic": "myplayer/set_mute",
  "command_play_topic": "myplayer/play",
  "command_play_payload": "Play",
  "command_pause_topic": "myplayer/pause",
  "command_pause_payload": "Pause",
  "command_playpause_topic": "myplayer/playpause",
  "command_playpause_payload": "PlayPause",
  "command_next_topic": "myplayer/next",
  "command_next_payload": "Next",
  "command_previous_topic": "myplayer/previous",
  "command_previous_payload": "Previous",
  "command_playmedia_topic": "myplayer/playmedia",
  "command_seek_topic": "myplayer/seek"
}
```


### Configuration Options

| Variable | Description | Topic | Payload |
|---|---|---|---|
| `name` | The name of the Media Player | - | - |
| `device` | Device registry info object (`identifiers`, `name`, etc.) | - | - |
| `availability` | Availability configuration object | - | - |
| ↳ `topic` | Availability status topic | `myplayer/available` | `online` / `offline` |
| ↳ `payload_available` | Payload when device is available | - | `online` *(default)* |
| ↳ `payload_not_available` | Payload when device is unavailable | - | `offline` *(default)* |
| `state_state_topic` | Media Player state topic | `myplayer/state` | `playing`, `paused`, `idle`, `off`, `stopped` |
| `state_title_topic` | Track title | `myplayer/title` | Track title string |
| `state_artist_topic` | Track artist | `myplayer/artist` | Track artist string |
| `state_album_topic` | Track album | `myplayer/album` | Track album string |
| `state_duration_topic` | Track duration in seconds | `myplayer/duration` | `int` (seconds) |
| `state_position_topic` | Track position in seconds | `myplayer/position` | `int` (seconds) |
| `state_volume_topic` | Current volume level | `myplayer/volume` | `0.0` - `1.0` (`float`) |
| `state_mute_topic` | Current mute state | `myplayer/mute` | `mute` / `unmute` |
| `state_albumart_topic` | Cover art image | `myplayer/albumart` | Base64-encoded image string |
| `state_mediatype_topic` | Media content type | `myplayer/mediatype` | `music`, `video`, etc. *(default: `music`)* |
| `command_volume_topic` | Set volume level | `myplayer/set_volume` | `0.0` - `1.0` (`float`) |
| `command_mute_topic` | Mute or unmute the player | `myplayer/set_mute` | `mute` / `unmute` |
| `command_play_topic` | Play media command topic | `myplayer/play` | `Play` *(or `command_play_payload`)* |
| `command_play_payload` | Payload sent on play command | - | `Play` *(default)* |
| `command_pause_topic` | Pause media command topic | `myplayer/pause` | `Pause` *(or `command_pause_payload`)* |
| `command_pause_payload` | Payload sent on pause command | - | `Pause` *(default)* |
| `command_playpause_topic` | Toggle play/pause command topic | `myplayer/playpause` | `PlayPause` *(or `command_playpause_payload`)* |
| `command_playpause_payload` | Payload sent on play/pause command | - | `PlayPause` *(default)* |
| `command_next_topic` | Skip to next track command topic | `myplayer/next` | `Next` *(or `command_next_payload`)* |
| `command_next_payload` | Payload sent on next track command | - | `Next` *(default)* |
| `command_previous_topic` | Skip to previous track command topic | `myplayer/previous` | `Previous` *(or `command_previous_payload`)* |
| `command_previous_payload` | Payload sent on previous track command | - | `Previous` *(default)* |
| `command_playmedia_topic` | Play media command topic | `myplayer/playmedia` | JSON `{"media_type": ..., "media_id": ...}` |
| `command_seek_topic` | Seek to a position in the current media | `myplayer/seek` | Position as a number, commonly seconds from the start |

### State Values

The `state_state_topic` should publish one of these values:
- `playing` - Media is currently playing
- `paused` - Media is paused
- `idle` - Player is idle
- `off` - Player is off
- `stopped` - Playback stopped

### Album Art

Album art should be published as a base64-encoded image (JPEG recommended) to the `state_albumart_topic`.

### Play Media

When media is played via Home Assistant (e.g. TTS or media browser), a JSON payload is published to `command_playmedia_topic`:
```json
{
  "media_type": "music",
  "media_id": "http://.../song.mp3"
}
```
