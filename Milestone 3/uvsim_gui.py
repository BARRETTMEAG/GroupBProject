import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from memory import Memory
from uvsim import UVSim
from convert import Convert
import builtins

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UVSim")
        self.sim = UVSim()
        self.output_lines = []
        self.build_widgets()

    def build_widgets(self):
        tk.Button(self.root, text="Load Program File", command=self.load_file).pack(pady=5)

        self.accumulator_var = tk.StringVar()
        tk.Label(self.root, text="Accumulator:").pack()
        tk.Entry(self.root, textvariable=self.accumulator_var, state='readonly').pack()

        mem_frame = tk.LabelFrame(self.root, text="Main Memory")
        mem_frame.pack(pady=10, fill="both", expand=True)

        self.mem_canvas = tk.Canvas(mem_frame)
        scrollbar = ttk.Scrollbar(mem_frame, orient="vertical", command=self.mem_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.mem_canvas.pack(side="left", fill="both", expand=True)
        self.mem_canvas.configure(yscrollcommand=scrollbar.set)

        self.mem_inner = tk.Frame(self.mem_canvas)
        self.mem_canvas.create_window((0, 0), window=self.mem_inner, anchor="nw")
        self.mem_inner.bind("<Configure>", lambda e: self.mem_canvas.configure(scrollregion=self.mem_canvas.bbox("all")))

        self.memory_labels = []
        for i in range(10):
            row = []
            for j in range(10):
                idx = i * 10 + j
                label = tk.Label(self.mem_inner, text=f"{idx:02}: 0000", width=12, relief="ridge", anchor="w")
                label.grid(row=i, column=j, sticky="nsew")
                row.append(label)
            self.memory_labels.append(row)

        tk.Label(self.root, text="Output:").pack()
        self.output_text = tk.Text(self.root, height=8, width=80, state='disabled')
        self.output_text.pack(pady=5)

        tk.Button(self.root, text="Run Program", command=self.run_program).pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                self.sim = UVSim()
                self.sim.load_program(file_path)
                self.sim.memory.read_callback = self.show_read_popup
                self.update_memory_display()
                self.accumulator_var.set(str(self.sim.cpu.accumulator))
                self.clear_output()
            except Exception as e:
                messagebox.showerror("Load Error", str(e))

    def run_program(self):
        try:
            self.sim.memory.read_callback = self.show_read_popup
            self.step_through_program()
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

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
        popup.title("UVSim")
        popup.geometry("300x150")
        popup.grab_set()

        tk.Label(popup, text="Enter the value to be stored:").pack(pady=10)
        input_entry = tk.Entry(popup)
        input_entry.pack()
        input_entry.focus_set()  # Ensure the input field is focused

        result = {"value": None}

        def submit():
            value = input_entry.get()
            try:
                int_value = Convert.convert_to_int(value)  # Validate input as an integer
                result["value"] = int_value
                self.sim.memory.write(operand, int_value)  # Store the value in memory
                popup.destroy()  # Close the popup
            except ValueError:
                messagebox.showerror("Invalid Input", "Enter an integer.")  # Show error message

        tk.Button(popup, text="Submit", command=submit).pack(pady=10)

        self.root.wait_window(popup)  # Wait for the popup to close
        return result["value"]

    def update_memory_display(self):
        for i in range(10):
            for j in range(10):
                idx = i * 10 + j
                val = self.sim.memory.read(idx)
                self.memory_labels[i][j].config(text=f"{idx:02}: {val:04}")

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


