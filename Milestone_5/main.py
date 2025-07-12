import tkinter as tk
from uvsim_gui import UVSimGUI

def main():
    root = tk.Tk()
    root.geometry("1024x768")
    UVSimGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
