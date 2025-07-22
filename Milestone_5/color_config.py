import json
import os
import re
import tkinter as tk
from tkinter import messagebox

class ColorConfig:
    HEX_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")

    def __init__(self, filename="colors.json"):
        self.filename = filename
        self.primary = "#4C721D"  # UVU dark green
        self.off = "#FFFFFF"      # UVU white
        self.load_colors()

    def is_valid_hex(self, value):
        return isinstance(value, str) and self.HEX_PATTERN.match(value)

    def show_error(self, title, message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()

    def load_colors(self):
        if not os.path.isfile(self.filename):
            self.show_error("ColorConfig Error",
                            f"File '{self.filename}' not found.\nUsing default colors.")
            return

        try:
            with open(self.filename, "r") as f:
                data = json.load(f)

            if "primary" in data:
                if self.is_valid_hex(data["primary"]):
                    self.primary = data["primary"]
                else:
                    self.show_error(
                        "ColorConfig Error",
                        f"Invalid hex value for 'primary' in {self.filename}.\nUsing default: {self.primary}"
                    )
            else:
                self.show_error(
                    "ColorConfig Error",
                    f"Missing 'primary' in {self.filename}.\nUsing default: {self.primary}"
                )

            if "off" in data:
                if self.is_valid_hex(data["off"]):
                    self.off = data["off"]
                else:
                    self.show_error(
                        "ColorConfig Error",
                        f"Invalid hex value for 'off' in {self.filename}.\nUsing default: {self.off}"
                    )
            else:
                self.show_error(
                    "ColorConfig Error",
                    f"Missing 'off' in {self.filename}.\nUsing default: {self.off}"
                )

        except json.JSONDecodeError:
            self.show_error(
                "ColorConfig Error",
                f"Failed to parse '{self.filename}'.\nPlease check JSON syntax.\nUsing default colors."
            )
        except Exception as e:
            self.show_error(
                "ColorConfig Error",
                f"Unexpected error: {e}\nUsing default colors."
            )
