import configparser
import re

HEX_RE = re.compile(r'^#[0-9A-Fa-f]{6}$')

class ColorConfig:
    def __init__(self, filename="colors.cfg"):
        self.filename = filename
        self.primary = "#4C721D"
        self.off = "#FFFFFF"
        self.load_colors()

    def load_colors(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.filename)
            prim = config.get("Colors", "primary", fallback=self.primary)
            off = config.get("Colors", "off", fallback=self.off)
            if HEX_RE.match(prim):
                self.primary = prim
            if HEX_RE.match(off):
                self.off = off
        except Exception:
            pass


