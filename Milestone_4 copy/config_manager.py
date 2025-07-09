import json, os

class ConfigManager:
    CONFIG_FILE = "config.json"
    DEFAULTS = {"primary_color": "#4C721D", "off_color": "#FFFFFF"}

    @classmethod
    def load_config(cls):
        if os.path.isfile(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    return {**cls.DEFAULTS, **data}
            except:
                pass
        return cls.DEFAULTS.copy()

    @classmethod
    def save_config(cls, config):
        with open(cls.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
