import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from memory import Memory
from uvsim import UVSim
from convert import Convert
from load import Load_Program
import builtins
from color_config import ColorConfig

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVSim")
        self.load = Load_Program()
        self.sim = UVSim()
        self.output_lines = []
        self.colors = ColorConfig()
        self.memory_entries = []
        self.file_loaded = False

        self.root.configure(bg=self.colors.primary)
        self.build_widgets()

    def build_widgets(self):
        top_frame = tk.Frame(self.root, bg=self.colors.primary)
        top_frame.pack(pady=10)

        tk.Button(top_frame, text="Load Program File", command=self.load_file, bg=self.colors.off).pack(side="left", padx=5)
        tk.Button(top_frame, text="Save Program File", command=self.save_file, bg=self.colors.off).pack(side="left", padx=5)

        self.run_button = tk.Button(top_frame, text="Run Program", command=self.run_program, bg=self.colors.off)
        self.run_button.pack(side="left", padx=5)

        self.accumulator_var = tk.StringVar()
        tk.Label(self.root, text="Accumulator:", bg=self.colors.primary, fg=self.colors.off).pack()
        tk.Entry(self.root, textvariable=self.accumulator_var, state='readonly').pack()

        mem_frame = tk.LabelFrame(self.root, text="Main Memory", bg=self.colors.primary, fg=self.colors.off)
        mem_frame.pack(pady=10, fill="both", expand=True)

        # Create a frame to hold both canvas and scrollbars
        canvas_frame = tk.Frame(mem_frame, bg=self.colors.primary)
        canvas_frame.pack(fill="both", expand=True)

        # Create the canvas
        self.mem_canvas = tk.Canvas(canvas_frame, bg=self.colors.primary)
        self.mem_canvas.pack(side="left", fill="both", expand=True)

        # Create vertical scrollbar
        scrollbarY = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.mem_canvas.yview)
        scrollbarY.pack(side="right", fill="y")

        # Create horizontal scrollbar
        scrollbarX = ttk.Scrollbar(mem_frame, orient="horizontal", command=self.mem_canvas.xview)
        scrollbarX.pack(fill="x")

        # Configure canvas to use scrollbars
        self.mem_canvas.configure(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)

        self.mem_inner = tk.Frame(self.mem_canvas, bg=self.colors.primary)
        self.mem_canvas.create_window((0, 0), window=self.mem_inner, anchor="nw")
        self.mem_inner.bind("<Configure>", lambda e: self.mem_canvas.configure(scrollregion=self.mem_canvas.bbox("all")))

        for i in range(16):
            tk.Label(self.mem_inner, text=f"{i:X}", bg=self.colors.primary, fg=self.colors.off, width=6).grid(row=0, column=i+1)
        for col in range(16):
            for row in range(16):
                idx = row + col * 16  # Column-wise increment
                if idx >= 250:
                    break

                # Address label (in a separate column before each entry)
                label = tk.Label(self.mem_inner, text=f"{idx:03}", width=4, anchor="e", bg=self.colors.primary, fg=self.colors.off)
                label.grid(row=row, column=col * 2, padx=(2, 0), pady=1)

                # Memory entry field
                entry = tk.Entry(self.mem_inner, width=10)
                entry.grid(row=row, column=col * 2 + 1, padx=(0, 5), pady=1)

                entry.insert(0, "+000000")
                entry.bind("<FocusOut>", lambda e, idx=idx: self.save_memory_entry(idx, e.widget.get()))
                self.memory_entries.append(entry)

        tk.Label(self.root, text="Output:", bg=self.colors.primary, fg=self.colors.off).pack()
        self.output_text = tk.Text(self.root, height=8, width=80, state='disabled')
        self.output_text.pack(pady=5)

    def load_file(self):
        if self.file_loaded:
            self.open_file_in_new_window()
            return
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                self.load = Load_Program()
                self.load.load_program(file_path)
                self.sim = UVSim(memory = self.load.memory)
                self.sim.memory.read_callback = self.show_read_popup
                self.update_memory_display()
                self.accumulator_var.set(str(self.sim.cpu.accumulator))
                self.clear_output()
                self.loaded_file_path = file_path
                self.file_loaded = True
            except Exception as e:
                messagebox.showerror("Load Error", str(e))

    def save_file(self):
        if not self.sync_entries_to_memory():
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    lines = []
                    for i in range(250):
                        val = self.sim.memory.read(i)
                        lines.append(f"{val:+07d}")
                    f.write("\n".join(lines))
                messagebox.showinfo("Success", f"Program saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def save_memory_entry(self, index, value):
        try:
            int_val = Convert.convert_to_int(value)
            if int_val is False:
                raise ValueError
            self.sim.memory.write(index, int_val)
        except Exception:
            messagebox.showerror("Invalid Input", f"Invalid value at memory [{index}]")

    def sync_entries_to_memory(self):
        for idx, entry in enumerate(self.memory_entries):
            if idx < 250:
                value = entry.get()
                try:
                    int_val = Convert.convert_to_int(value)
                    if int_val is False or not isinstance(int_val, int):
                        raise ValueError
                    self.sim.memory.write(idx, int_val)
                except Exception:
                    messagebox.showerror("Invalid Input", f"Invalid value at memory [{idx}] during sync.")
                    return False
        return True
    
    def run_program(self):
        if not self.sync_entries_to_memory():
            return

        self.sim.cpu.program_counter = 0
        self.sim.cpu.halted = False
        self.sim.cpu.accumulator = 0

        self.run_button.config(state='disabled')
        try:
            self.sim.memory.read_callback = self.show_read_popup
            self.step_through_program()
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))
        finally:
            self.run_button.config(state='normal')

    def step_through_program(self):
        original_print = builtins.print
        output = []

        def capture_print(*args, **kwargs):
            line = " ".join(str(a) for a in args)
            output.append(line)
            original_print(*args, **kwargs)

        builtins.print = capture_print
        while not self.sim.cpu.halted:
            instruction = self.sim.memory.read(self.sim.cpu.program_counter)
            self.sim.cpu.execute(instruction, self.sim.memory)
            if self.sim.memory.waiting_for_input:
                break
        builtins.print = original_print

        self.output_lines.extend(output)
        self.update_output()
        self.update_memory_display()
        self.accumulator_var.set(str(self.sim.cpu.accumulator))

    def show_read_popup(self, operand):
        popup = tk.Toplevel(self.root)
        popup.title("UVSim Input")
        popup.geometry("300x150")
        popup.grab_set()

        tk.Label(popup, text="Enter the value to be stored:").pack(pady=10)
        input_entry = tk.Entry(popup)
        input_entry.pack()
        input_entry.focus_set()

        result = {"value": None}

        def submit():
            value = input_entry.get()
            if value.strip() == "":
                messagebox.showwarning("Input Warning", "Blank input interpreted as 0.")
                int_value = 0
            else:
                try:
                    int_value = int(value)
                    if int_value < -999999 or int_value > 999999:
                        messagebox.showwarning("Input Warning", "Value truncated to 6-digit range.")
                        int_value = int_value % 1000000
                except ValueError:
                    messagebox.showerror("Invalid Input", "Enter a valid integer.")
                    return
            self.sim.memory.write(operand, int_value)
            result["value"] = int_value
            popup.destroy()

        tk.Button(popup, text="Submit", command=submit).pack(pady=10)
        self.root.wait_window(popup)
        return result["value"]

    def update_memory_display(self):
        for i in range(250):
            val = self.sim.memory.read(i)
            self.memory_entries[i].delete(0, tk.END)
            self.memory_entries[i].insert(0, f"{val:+07d}")

    def update_output(self):
        self.output_text.configure(state='normal')
        self.output_text.delete("1.0", tk.END)
        for line in self.output_lines:
            self.output_text.insert(tk.END, line + "\n")
        self.output_text.configure(state='disabled')

    def clear_output(self):
        self.output_lines = []
        self.output_text.configure(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state='disabled')

    def open_file_in_new_window(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                new_root = tk.Toplevel(self.root)
                new_gui = UVSimGUI(new_root)
                new_gui.load = Load_Program()
                new_gui.load.load_program(file_path)
                new_gui.sim = UVSim(memory=new_gui.load.memory)
                new_gui.sim.memory.read_callback = new_gui.show_read_popup
                new_gui.update_memory_display()
                new_gui.accumulator_var.set(str(new_gui.sim.cpu.accumulator))
                new_gui.clear_output()
                new_gui.loaded_file_path = file_path
                new_gui.file_loaded = True
                new_root.title("UVSim")
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load {file_path}:\n{str(e)}")
