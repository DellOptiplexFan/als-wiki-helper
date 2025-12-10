import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import csv
from io import StringIO
import re
import sv_ttk # type: ignore
import darkdetect # type: ignore

def format_number(num_str):
    return num_str.strip()

def parse_csv_to_template(csv_text):
    lines = csv_text.strip().split('\n')
    reader = csv.reader(lines)
    rows = list(reader)
    
    column_header_row = None
    for i, row in enumerate(rows):
        if any('Upgrade #' in str(cell) for cell in row):
            column_header_row = i
            break
    
    if column_header_row is None:
        return "column header not found"
    
    header_row = rows[column_header_row]
    unit_starts = []
    
    for i, cell in enumerate(header_row):
        if 'Upgrade #' in str(cell):
            unit_starts.append(i)
    
    valid_unit_data = None
    
    for unit_idx, start_col in enumerate(unit_starts):
        end_col = unit_starts[unit_idx + 1] if unit_idx + 1 < len(unit_starts) else len(header_row)
        
        headers = []
        for col_idx in range(start_col, end_col):
            if col_idx < len(header_row):
                header = str(header_row[col_idx]).strip()
                if header:
                    headers.append((col_idx, header))
        
        upgrades = []
        for row_idx in range(column_header_row + 1, len(rows)):
            row = rows[row_idx]
            
            upgrade = {}
            for col_idx, header in headers:
                if col_idx < len(row):
                    value = str(row[col_idx]).strip()
                    if value:
                        upgrade[header] = value
            
            if 'Upgrade #' in upgrade and 'Cost' in upgrade:
                cost = upgrade.get('Cost', '').replace(' ', '').replace(',', '')
                if cost and cost != '0' and cost != '':
                    upgrades.append(upgrade)
        
        if upgrades and valid_unit_data is None:
            valid_unit_data = upgrades
            break
    
    if not valid_unit_data:
        return "unit data not found. did you input it?"
    
    result = ["{{Main Stats Outer Shell|"]
    
    previous_aoe = None
    
    for upgrade in valid_unit_data:
        damage = upgrade.get('Damage', '').replace(',', '').replace(' ', '')
        if damage == '0' or damage == '':
            continue
        
        parts = ["{{Stats Box"]
        extra_lines = []
        
        if 'Cost' in upgrade:
            cost = format_number(upgrade['Cost'])
            parts.append(f"|Upgrade_Cost={cost}")
        
        if 'Upgrade #' in upgrade:
            parts.append(f"|Upgrade_No={upgrade['Upgrade #']}")
        
        if 'Damage' in upgrade:
            damage_val = format_number(upgrade['Damage'])
            if damage_val and damage_val != '0':
                parts.append(f"|Damage={damage_val}")
        
        if 'Range' in upgrade and upgrade['Range']:
            parts.append(f"|Range={upgrade['Range']}")
        
        if 'SPA' in upgrade and upgrade['SPA']:
            parts.append(f"|SPA={upgrade['SPA']}")
        
        has_attack_name = 'Attack Name' in upgrade and upgrade['Attack Name']
        
        if has_attack_name:
            extra_lines.append(f"|Tower_Type={upgrade.get('Tower Type', 'Hybrid')} ")
            
            current_aoe = upgrade.get('AoE Type', '')
            extra_lines.append(f"|Attack_Type=AoE ({current_aoe})")
            
            extra_lines.append(f"|Text_Line_1='''{upgrade['Attack Name']}'''")
            
            status_effects = []
            if 'Status Effect 1' in upgrade and upgrade['Status Effect 1']:
                status_effects.append(upgrade['Status Effect 1'])
            if 'Status Effect 2' in upgrade and upgrade['Status Effect 2']:
                status_effects.append(upgrade['Status Effect 2'])
            
            if status_effects:
                status_text = "Attack inflict " + " and ".join([f"{{{{Passive|{s}}}}}" for s in status_effects])
                extra_lines.append(f"|Text_Line_2='''{status_text}'''")
            
            if previous_aoe and previous_aoe != current_aoe:
                extra_lines.append(f"|AoE_Change=AoE ({current_aoe})")
            
            previous_aoe = current_aoe
        
        if extra_lines:
            result.append(''.join(parts))
            result.extend(extra_lines)
            result.append("}}")
        else:
            result.append(''.join(parts) + "}}")
    
    result.append("}}")
    
    return '\n'.join(result)

def convert_to_html(text: str) -> str:
    output_lines = []
    in_ul = False
    for line in text.splitlines():
        if line and line[0] == "-":
            if in_ul == False:
                in_ul = True
                output_lines.append("<ul>")
            output_lines.append("<li>" + line[1:] + "</li>")
        else:
            if in_ul == True:
                output_lines.append("</ul>")
                in_ul = False
            output_lines.append("<div>" + line + "</div>")
    if in_ul == True:
        output_lines.append("</ul>")
    return "\n".join(line for line in output_lines)

def status_effects(text:str) -> str:
    status_effect_list = {
        "Bleed": "{{Passive|Bleed}}",
        "Flame": "{{Passive|Flame}}",
        "Cripple": "{{Passive|Cripple}}",
        "Dismantle": "{{Passive|Dismantle}}",
        "Fear": "{{Passive|Fear}}",
        "Freeze": "{{Passive|Freeze}}",
        "Poison": "{{Passive|Poison}}",
        "Slow": "{{Passive|Slow}}",
        "Electrified": "{{Passive|Electrified}}",
        "Stun": "{{Passive|Stun}}",
        "Conquered": "{{Passive|Conquered}}",
        "Hemorrhage": "{{Passive|Hemorrhage}}",
        "Black Flames": "{{Passive|Black Flame}}",
        "Bomb": "{{Passive|Bomb}}",
        "Detonation": "{{Passive|Detonation}}",
        "Random": "{{Passive|Random}}",
        "Frostbite": "{{Passive|Frostbite}}",
        "Pressure": "{{Passive|Pressure}}",
        "Blizzard": "{{Passive|Blizzard}}",
        "Bolt": "{{Passive|Bolt}}",
        "Mutilate": "{{Passive|Mutilate}}",
        "Sunburn": "{{Passive|Sunburn}}",
        "Weakened": "{{Passive|Weakened}}",
        "Blue Flames": "{{Passive|Blue Flames}}",
        "Plasma": "{{Passive|Plasma}}",
        "Accelerate": "{{Passive|Accelerate}}",
        "Scorched": "{{Passive|Scorched}}",
        "WindSheer": "{{Passive|WindSheer}}",
        "Soaked": "{{Passive|Soaked}}",
        "AntiMagic": "{{Passive|AntiMagic}}",
        "Despair": "{{Passive|Despair}}",
        "Blaze": "{{Passive|Blaze}}",
        "Petrification": "{{Passive|Petrification}}",
        "Extinguish": "{{Passive|Extinguish}}",
        "Rupture": "{{Passive|Rupture}}",
        "Exposed": "{{Passive|Exposed}}",
        "Bloodlust": "{{Passive|Bloodlust}}",
        "Solar Flames": "{{Passive|Solar Flames}}",
        "Unstable": "{{Passive|Unstable}}",
        "Shred": "{{Passive|Shred}}",
        "Brittle": "{{Passive|Brittle}}",
        "Daze": "{{Passive|Daze}}",
        "Restrict": "{{Passive|Restrict}}",
    }

    status_effects_sorted = sorted(status_effect_list.keys(), key=len, reverse=True)
    for effect in status_effects_sorted:
        template = status_effect_list[effect]
        pattern = re.compile(rf'\b({re.escape(effect)})\b', re.IGNORECASE)
        text = pattern.sub(lambda m: template if not re.search(r'\{\{Passive\|', text[:text.find(m.group())]) else m.group(), text)
    return text



def color_brackets(text: str) -> str:
    output_lines = []
    for line in text.splitlines():
        new_line = ""
        counter = 0
        for char in line:
            if char in ["(","["]:
                if counter == 0:
                    new_line = new_line + ' <span style="color:grey;">' + char
                else:
                    new_line = new_line + char
                counter += 1
            elif char in [")","]"]:
                counter -= 1
                new_line = new_line + char
                if counter == 0:
                    new_line = new_line + '</span> '
            else:
                new_line = new_line + char
        output_lines.append(new_line)
    return "\n".join(line for line in output_lines)
            
def color_numbers(text: str, color: str) -> str:
    pattern = re.compile(
        r"""
        (?<![#])                      # not preceded by '#'
        (?<!\w)                       # not preceded by a letter/digit
        (                             
            [+\-]?                    # optional sign
            (?:\d+(\.\d+)?|\.\d+)     # 12, 12.34, or .45
            (?:%|[skMBT])?            # Optional %, s, k, M, B, T
        )
        (?!\w)                        # Not followed by a letter/digit
        """,
        re.VERBOSE
    )
    output_lines = [pattern.sub(rf'<span style="color:{color};"> \1 </span>', line) for line in text.splitlines()]
    return "\n".join(line for line in output_lines)

def colorize(text: str, color: str) -> str:
    text = color_brackets(text)
    text = color_numbers(text, color)
    return text

def full_convert_passive(text: str) -> str:
    text = status_effects(text)
    text = convert_to_html(text)
    text = colorize(text, "cyan")
    return text

def full_convert_ability(text: str) -> str:
    text = status_effects(text)
    text = convert_to_html(text)
    text = colorize(text, "red")
    return text

# I lowkey vibecoded this gui shit LOL idk how to use tkinter
class converter_gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Wiki Converter Tool")
        self.root.geometry("1100x850")
        
        # Apply sv_ttk theme and set colors based on system theme
        is_dark = darkdetect.isDark()
        sv_ttk.set_theme("dark" if is_dark else "light")
        
        # Set text widget colors based on theme
        self.text_bg = "#212121" if is_dark else "#ffffff"
        self.text_fg = "#ffffff" if is_dark else "#000000"
        self.cursor_color = "#0d7377"
        
        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=16, pady=16)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Wiki Converter Tool", 
                               font=("Segoe UI", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Conversion type selection
        type_frame = ttk.LabelFrame(main_frame, text="Conversion Type", padding=12)
        type_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 16))
        
        self.conversion_type = tk.StringVar(value="stats")
        
        for text, value in [("Stats", "stats"), ("Passive", "passive"), ("Ability", "ability")]:
            ttk.Radiobutton(type_frame, text=text, variable=self.conversion_type, value=value).pack(side=tk.LEFT, padx=12)
        
        # Input area
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding=12)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 12))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        input_scroll = ttk.Scrollbar(input_frame)
        input_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.input_text = tk.Text(input_frame, wrap=tk.WORD, 
                                 width=100, height=12,
                                 font=("Consolas", 10),
                                 yscrollcommand=input_scroll.set,
                                 bg=self.text_bg, fg=self.text_fg,
                                 insertbackground=self.cursor_color,
                                 relief=tk.FLAT, bd=0)
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_scroll.config(command=self.input_text.yview)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=12, sticky=(tk.W, tk.E))
        
        buttons = [
            ("Convert", self.convert),
            ("Clear Input", self.clear_input),
            ("Clear Output", self.clear_output),
            ("Copy Output", self.copy_output)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=6)
        
        # Output area
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding=12)
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        output_scroll = ttk.Scrollbar(output_frame)
        output_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, 
                                  width=100, height=12,
                                  font=("Consolas", 10),
                                  yscrollcommand=output_scroll.set,
                                  bg=self.text_bg, fg=self.text_fg,
                                  insertbackground=self.cursor_color,
                                  relief=tk.FLAT, bd=0)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_scroll.config(command=self.output_text.yview)

        
        
    def convert(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        
        if not input_data:
            messagebox.showwarning("Warning", "Please enter some input text!")
            return
        
        conversion = self.conversion_type.get()
        
        try:
            if conversion == "stats":
                output = parse_csv_to_template(input_data)
            elif conversion == "passive":
                output = full_convert_passive(input_data)
            elif conversion == "ability":
                output = full_convert_ability(input_data)
            else:
                output = "Invalid conversion type"
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", output)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during conversion:\n{str(e)}")
    
    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
    
    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
    
    def copy_output(self):
        output_data = self.output_text.get("1.0", tk.END).strip()
        if output_data:
            self.root.clipboard_clear()
            self.root.clipboard_append(output_data)
            messagebox.showinfo("Success", "Output copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No output to copy!")

def main():
    root = tk.Tk()
    app = converter_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()