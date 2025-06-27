import tkinter as tk
from uvsim_gui import UVSimGUI

def main():
    root = tk.Tk()
    UVSimGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
