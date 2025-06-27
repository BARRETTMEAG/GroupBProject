import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
from uvsim import UVSim
from convert import Convert
from config_manager import ConfigManager

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVSim")
        self.sim = UVSim()
        self.output_lines = []
        self.config = ConfigManager.load_config()
        self.build_widgets()
        self.apply_colors()

    def apply_colors(self):
        p, o = self.config["primary_color"], self.config["off_color"]
        self.root.configure(bg=p)
        for btn in self.root.winfo_children():
            if isinstance(btn, tk.Button):
                btn.configure(bg=p, fg=o)
        # Similar application for other widget types...

    def build_widgets(self):
        # Top toolbar
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill="x", pady=5)
        tk.Button(toolbar, text="Load Program", command=self.load_file).pack(side="left", padx=2)
        tk.Button(toolbar, text="Save Program", command=self.save_file).pack(side="left", padx=2)
        tk.Button(toolbar, text="Pick Colors", command=self.pick_colors).pack(side="left", padx=2)
        self.run_button = tk.Button(toolbar, text="Run Program", command=self.run_program, state="disabled")
        self.run_button.pack(side="left", padx=2)

        # Editable memory list view
        self.mem_tree = ttk.Treeview(self.root, columns=("value",), show="headings", selectmode="browse")
        self.mem_tree.heading("value", text="Instruction/Data")
        self.mem_tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.mem_tree.bind("<Double-1>", self.edit_memory_cell)

        # Output view
        tk.Label(self.root, text="Output:").pack()
        self.output_text = tk.Text(self.root, height=8, width=80, state="disabled")
        self.output_text.pack(pady=5)

    def pick_colors(self):
        p = colorchooser.askcolor(self.config["primary_color"])[1]
        o = colorchooser.askcolor(self.config["off_color"])[1]
        if p and o:
            self.config.update({"primary_color": p, "off_color": o})
            ConfigManager.save_config(self.config)
            self.apply_colors()

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        if path:
            self.sim = UVSim()
            try:
                self.sim.load_program(path)
            except Exception as e:
                return messagebox.showerror("Load Error", str(e))
            self.populate_tree()
            self.run_button.config(state="normal")
            self.output_text.config(state="normal"); self.output_text.delete("1.0","end"); self.output_text.config(state="disabled")

    def populate_tree(self):
        self.mem_tree.delete(*self.mem_tree.get_children())
        for i, val in enumerate(self.sim.memory.memory):
            self.mem_tree.insert("", "end", iid=str(i), values=(f"{i:02}: {val:04}",))

    def edit_memory_cell(self, event):
        iid = self.mem_tree.focus()
        if not iid: return
        col = self.mem_tree.identify_column(event.x)
        if col != "#1": return
        old = self.mem_tree.item(iid, "values")[0].split(": ")[1]
        new = tk.simpledialog.askstring("Edit cell", f"Enter new value for {iid}", initialvalue=old)
        if new is not None:
            try:
                iv = Convert.convert_to_int(new)
                if iv is False: raise ValueError
                self.sim.memory.write(int(iid), iv)
                self.mem_tree.item(iid, values=(f"{int(iid):02}: {iv:04}",))
            except:
                messagebox.showerror("Invalid Input", "Please enter a signed 4-digit integer.")

    def save_file(self):
        if not self.sim:
            return messagebox.showinfo("Info", "No program loaded.")
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if path:
            lines = [f"{v:04}\n" for v in self.sim.memory.memory if v != 0]
            try:
                with open(path, "w") as f: f.writelines(lines)
                messagebox.showinfo("Saved", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def run_program(self):
        self.sim.reset()
        self.output_lines = []
        try:
            while not self.sim.cpu.halted:
                self.sim.step()
        except Exception as e:
            messagebox.showerror("Runtime Error", str(e))
        self.update_output()
        self.populate_tree()

    def update_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0","end")
        for line in self.output_lines:
            self.output_text.insert("end", line+"\n")
        self.output_text.config(state="disabled")
