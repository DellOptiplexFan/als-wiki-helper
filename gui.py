import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import darkdetect

from converters.stat_converter import parse_csv_to_template
from converters.ability_converter import full_convert_passive, full_convert_ability


class ConverterGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Wiki Converter Tool")
        self.root.geometry("400x220")
        sv_ttk.set_theme("dark" if darkdetect.isDark() else "light")

        self.build_main_menu()

    # ---------------------------
    # MAIN MENU
    # ---------------------------
    def build_main_menu(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Wiki Converter Tool",
                  font=("Segoe UI", 22, "bold")).pack(pady=10)

        ttk.Button(
            frame, text="Stats Converter", width=30,
            command=self.open_stats_window
        ).pack(pady=10)

        ttk.Button(
            frame, text="Ability / Passive Converter", width=30,
            command=self.open_ability_window
        ).pack(pady=10)

    # ---------------------------
    # STATS WINDOW
    # ---------------------------
    def open_stats_window(self):
        win = tk.Toplevel(self.root)
        win.title("Stats Converter")
        win.geometry("600x650")

        container = ttk.Frame(win, padding=20)
        container.pack(expand=True, fill="both")

        # Title
        ttk.Label(container, text="Stats Converter",
                  font=("Segoe UI", 18, "bold")).pack(pady=10)

        # Input field at top
        ttk.Label(container, text="CSV Input:").pack(anchor="w", pady=(10, 5))
        
        input_frame = ttk.Frame(container)
        input_frame.pack(fill="both", expand=False, pady=(0, 10))
        
        scroll_in = ttk.Scrollbar(input_frame)
        scroll_in.pack(side="right", fill="y")
        
        self.stats_input_box = tk.Text(
            input_frame, height=6, wrap="word", font=("Consolas", 10)
        )
        self.stats_input_box.pack(fill="both", expand=True)
        scroll_in.config(command=self.stats_input_box.yview)
        self.stats_input_box.config(yscrollcommand=scroll_in.set)

        # Store reference for convert_stats method
        self.stats_entries = {"CSV Input": self.stats_input_box}

        # Button frame
        button_frame = ttk.Frame(container)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(
            button_frame, text="Paste Input",
            command=lambda: self.paste_input()
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Copy Output",
            command=lambda: self.copy_output()
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Clear",
            command=lambda: self.clear_stats()
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Convert",
            command=lambda: self.convert_stats(container)
        ).pack(side="left", padx=5)

        # Output box
        ttk.Label(container, text="Output:").pack(anchor="w", pady=(10, 5))
        
        output_frame = ttk.Frame(container)
        output_frame.pack(fill="both", expand=True)
        
        scroll_out = ttk.Scrollbar(output_frame)
        scroll_out.pack(side="right", fill="y")
        
        self.stats_output_box = tk.Text(
            output_frame, height=12, wrap="word", font=("Consolas", 10)
        )
        self.stats_output_box.pack(fill="both", expand=True)
        scroll_out.config(command=self.stats_output_box.yview)
        self.stats_output_box.config(yscrollcommand=scroll_out.set)
        self.stats_output_box.config(state="disabled")

    def paste_input(self):
        """Paste clipboard content into stats input box."""
        try:
            clipboard_text = self.root.clipboard_get()
            self.stats_input_box.insert(tk.END, clipboard_text)
        except tk.TclError:
            messagebox.showwarning("Warning", "Clipboard is empty or unavailable.")

    def copy_output(self):
        """Copy stats output box content to clipboard."""
        try:
            output_text = self.stats_output_box.get("1.0", tk.END)
            if output_text.strip():
                self.root.clipboard_clear()
                self.root.clipboard_append(output_text)
                messagebox.showinfo("Success", "Output copied to clipboard!")
            else:
                messagebox.showwarning("Warning", "Output is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy output:\n{e}")

    def clear_stats(self):
        """Clear the stats input box."""
        self.stats_input_box.delete("1.0", tk.END)

    def convert_stats(self, container):
        try:
            csv_text = self.stats_input_box.get("1.0", tk.END)
            result = parse_csv_to_template(csv_text)

            self.stats_output_box.config(state="normal")
            self.stats_output_box.delete("1.0", tk.END)
            self.stats_output_box.insert("1.0", result)
            self.stats_output_box.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{e}")

    # ---------------------------
    # ABILITY/PASSIVE WINDOW
    # ---------------------------
    def open_ability_window(self):
        win = tk.Toplevel(self.root)
        win.title("Ability / Passive Converter")
        win.geometry("600x650")

        container = ttk.Frame(win, padding=20)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Ability / Passive Converter",
                  font=("Segoe UI", 18, "bold")).pack(pady=10)

        # Mode selection
        self.ability_mode = tk.StringVar(value="ability")
        self.ability_mode.trace("w", lambda *args: self.update_ability_fields())

        mode_frame = ttk.Frame(container)
        mode_frame.pack()

        ttk.Radiobutton(
            mode_frame, text="Ability", variable=self.ability_mode, value="ability"
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            mode_frame, text="Passive", variable=self.ability_mode, value="passive"
        ).pack(side="left", padx=10)

        # --- Extra Fields Frame (Name, Cooldown, Upgrade) ---
        self.extra_frame = ttk.Frame(container)
        self.extra_frame.pack(fill="x", pady=10)

        # Row: Name
        self.row_name = ttk.Frame(self.extra_frame)
        ttk.Label(self.row_name, text="Name:", width=15).pack(side="left")
        self.entry_name = ttk.Entry(self.row_name)
        self.entry_name.pack(side="left", fill="x", expand=True)

        # Row: Cooldown (only for abilities)
        self.row_cd = ttk.Frame(self.extra_frame)
        ttk.Label(self.row_cd, text="Cooldown:", width=15).pack(side="left")
        self.entry_cooldown = ttk.Entry(self.row_cd)
        self.entry_cooldown.pack(side="left", fill="x", expand=True)

        # Row: Upgrade
        self.row_up = ttk.Frame(self.extra_frame)
        ttk.Label(self.row_up, text="Upgrade:", width=15).pack(side="left")
        self.entry_upgrade = ttk.Entry(self.row_up)
        self.entry_upgrade.pack(side="left", fill="x", expand=True)

        # Initialize correct layout
        self.update_ability_fields()

        # ---- MULTILINE INPUT FIELD ----
        ttk.Label(container, text="Input Text:").pack(pady=(15, 5))

        input_frame = ttk.Frame(container)
        input_frame.pack(fill="both", expand=False)

        scroll_in = ttk.Scrollbar(input_frame)
        scroll_in.pack(side="right", fill="y")

        self.ability_input = tk.Text(
            input_frame, height=8, wrap="word", font=("Consolas", 10)
        )
        self.ability_input.pack(fill="both", expand=True)
        scroll_in.config(command=self.ability_input.yview)
        self.ability_input.config(yscrollcommand=scroll_in.set)

        # Convert button
        ttk.Button(
            container, text="Convert",
            command=lambda: self.convert_ability(container)
        ).pack(pady=10)

        # Output box
        self.ability_output_box = tk.Text(container, height=12, wrap="word")
        self.ability_output_box.pack(fill="both", expand=True, pady=10)
        self.ability_output_box.config(state="disabled")


    def update_ability_fields(self):
        mode = self.ability_mode.get()

        # Hide all rows first
        self.row_name.pack_forget()
        self.row_cd.pack_forget()
        self.row_up.pack_forget()

        # Always show Name
        self.row_name.pack(fill="x", pady=3)

        # Cooldown only in ability mode
        if mode == "ability":
            self.row_cd.pack(fill="x", pady=3)

        # Always show Upgrade
        self.row_up.pack(fill="x", pady=3)


    def convert_ability(self, container):
        """Run ability/passive converter with additional fields."""
        text = self.ability_input.get("1.0", tk.END).strip()
        name = self.entry_name.get().strip()
        cooldown = self.entry_cooldown.get().strip()
        upgrade = self.entry_upgrade.get().strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter ability or passive text.")
            return

        if not name:
            messagebox.showwarning("Warning", "Please enter a name.")
            return

        mode = self.ability_mode.get()

        try:
            if mode == "passive":
                result = full_convert_passive(text, name=name, upgrade=upgrade)
            else:
                result = full_convert_ability(
                    text, name=name, cooldown=cooldown, upgrade=upgrade
                )

            self.ability_output_box.config(state="normal")
            self.ability_output_box.delete("1.0", tk.END)
            self.ability_output_box.insert("1.0", result)
            self.ability_output_box.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    ConverterGUI(root)
    root.mainloop()
