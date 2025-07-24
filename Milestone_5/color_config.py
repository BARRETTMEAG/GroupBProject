import json
import os
import re

class ColorConfig:
    HEX_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")

    def __init__(self, filename="colors.json"):
        self.filename = filename
        self.primary = "#4C721D"  # UVU dark green
        self.off = "#FFFFFF"      # UVU white
        self.load_colors()

    def is_valid_hex(self, value):
        return isinstance(value, str) and self.HEX_PATTERN.match(value)

    def load_colors(self):
        if not os.path.isfile(self.filename):
            print(f"[ColorConfig] File '{self.filename}' not found. Using default colors.")
            return

        try:
            with open(self.filename, "r") as f:
                data = json.load(f)

            if "primary" in data and self.is_valid_hex(data["primary"]):
                self.primary = data["primary"]
            else:
                print(f"[ColorConfig] Invalid or missing 'primary' in {self.filename}. Using default: {self.primary}")

            if "off" in data and self.is_valid_hex(data["off"]):
                self.off = data["off"]
            else:
                print(f"[ColorConfig] Invalid or missing 'off' in {self.filename}. Using default: {self.off}")

        except json.JSONDecodeError:
            print(f"[ColorConfig] Failed to parse '{self.filename}'. Please check JSON syntax. Using default colors.")
        except Exception as e:
            print(f"[ColorConfig] Unexpected error: {e}. Using default colors.")

