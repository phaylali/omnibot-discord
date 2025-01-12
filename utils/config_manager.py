import json
import os

class ConfigManager:
    def __init__(self):
        self.config_file = "config.json"
        self.config = {
            "monitored_channels": {
                "twitch": {},
                "youtube": {},
                "trovo": {}
            },
            "status_channels": []
        }
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.save_config()
        else:
            with open(self.config_file, 'r') as f:
                loaded_config = json.load(f)
                # Ensure monitored_channels exists in loaded config
                if "monitored_channels" not in loaded_config:
                    loaded_config["monitored_channels"] = {
                        "twitch": {},
                        "youtube": {},
                        "trovo": {}
                    }
                self.config = loaded_config

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_monitored_channels(self):
        return self.config["monitored_channels"]

    def get_status_channels(self):
        return self.config["status_channels"]

    def add_monitored_channel(self, platform, channel_name, discord_channel_id):
        if platform not in self.config["monitored_channels"]:
            self.config["monitored_channels"][platform] = {}
        self.config["monitored_channels"][platform][channel_name] = discord_channel_id
        self.save_config()

    def remove_monitored_channel(self, platform, channel_name):
        if platform in self.config["monitored_channels"]:
            if channel_name in self.config["monitored_channels"][platform]:
                del self.config["monitored_channels"][platform][channel_name]
                self.save_config()
                return True
        return False

    def add_status_channel(self, channel_id: int):
        if channel_id not in self.config['status_channels']:
            self.config['status_channels'].append(channel_id)
            self.save_config()
            return True
        return False

    def remove_status_channel(self, channel_id: int):
        if channel_id in self.config['status_channels']:
            self.config['status_channels'].remove(channel_id)
            self.save_config()
            return True
        return False