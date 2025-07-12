import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from load import Load_Program
from uvsim import UVSim
from color_config import ColorConfig
from convert import Convert

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.colors = ColorConfig()
        self.root.configure(bg=self.colors.primary)
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill="both")
        self.open_tabs = {}
        self.build_menu()

    def build_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Load Program...", command=self.load_file)
        filemenu.add_command(label="Convert 4‑digit to 6‑digit...", command=self.convert_file_dialog)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not path:
            return
        loader = Load_Program()
        try:
            loader.load_program(path)
        except Exception as e:
            messagebox.showerror("Error", str(e)); return

        self.add_tab(path, loader.memory)

    def convert_file_dialog(self):
        from file_converter import FileConverter
        inp = filedialog.askopenfilename(title="Old-format file", filetypes=[("Text files", "*.txt")])
        out = filedialog.asksaveasfilename(title="Save new-format file", defaultextension=".txt")
        if inp and out:
            try:
                FileConverter.convert_file(inp, out)
                messagebox.showinfo("Success", f"Saved converted file to {out}")
            except Exception as e:
                messagebox.showerror("Conversion Error", str(e))

    def add_tab(self, path, memory):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=path.split("/")[-1])
        gui = SingleFileTab(tab, path, memory, self.colors)
        self.open_tabs[path] = gui
        self.tab_control.select(tab)

class SingleFileTab:
    def __init__(self, parent, filepath, memory, colors):
        self.memory = memory
        self.colors = colors
        self.sim = UVSim(memory=memory)
        self.build_widgets(parent)
        self.update_memory_display()

    def build_widgets(self, parent):
        top = tk.Frame(parent, bg=self.colors.primary)
        top.pack(pady=5)
        load_btn = tk.Button(top, text="Run", command=self.run, bg=self.colors.off)
        load_btn.pack(side="left", padx=5)
        save_btn = tk.Button(top, text="Save...", command=self.save, bg=self.colors.off)
        save_btn.pack(side="left", padx=5)

        self.mem_canvas = tk.Canvas(parent, bg=self.colors.primary)
        sb = ttk.Scrollbar(parent, orient="vertical", command=self.mem_canvas.yview)
        sb.pack(side="right", fill="y")
        self.mem_canvas.pack(side="left", fill="both", expand=True)
        self.mem_canvas.configure(yscrollcommand=sb.set)

        self.mem_inner = tk.Frame(self.mem_canvas, bg=self.colors.primary)
        self.mem_canvas.create_window((0, 0), window=self.mem_inner, anchor="nw")
        self.mem_inner.bind("<Configure>", lambda e: self.mem_canvas.configure(scrollregion=self.mem_canvas.bbox("all")))

        self.entries = []
        rows = 25
        cols = 10
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                lbl = tk.Label(self.mem_inner, text=f"{idx:03d}", width=5, bg=self.colors.primary, fg=self.colors.off)
                lbl.grid(row=r, column=c*2)
                e = tk.Entry(self.mem_inner, width=8)
                e.grid(row=r, column=c*2+1)
                e.insert(0, "+000000")
                e.bind("<FocusOut>", lambda ev, idx=idx: self.update_memory(idx, ev.widget.get()))
                self.entries.append(e)

    def update_memory(self, idx, text):
        val = Convert.convert_to_int(text)
        if val is False:
            messagebox.showerror("Invalid Input", f"Entry at {idx:03d} is not an integer")
            return
        try:
            self.memory.write(idx, val)
        except Exception as e:
            messagebox.showerror("Write Error", str(e))

    def update_memory_display(self):
        for i in range(250):
            val = self.memory.read(i)
            display = f"{val:+07d}" if val >= 0 else f"{val:+07d}"
            self.entries[i].delete(0, "end")
            self.entries[i].insert(0, display)

    def run(self):
        self.sim.cpu.program_counter = 0
        self.sim.cpu.accumulator = 0
        self.sim.cpu.halted = False
        try:
            self.sim.run()
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))
        self.update_memory_display()

    def save(self):
        from tkinter import filedialog
        fp = filedialog.asksaveasfilename(defaultextension=".txt")
        if not fp:
            return
        try:
            with open(fp, "w") as f:
                for i in range(250):
                    w = self.memory.read(i)
                    f.write(f"{w:+07d}\n")
            messagebox.showinfo("Saved", f"Saved to {fp}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
