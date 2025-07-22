import configparser

class ColorConfig:
    def __init__(self, filename="colors.cfg"):
        self.filename = filename
        self.primary = "#4C721D"  # UVU dark green
        self.off = "#FFFFFF"      # UVU white
        self.load_colors()

    def load_colors(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.filename)
            self.primary = config.get("Colors", "primary", fallback=self.primary)
            self.off = config.get("Colors", "off", fallback=self.off)
        except Exception:
            pass
