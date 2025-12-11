import tkinter as tk
import sv_ttk
import darkdetect
from gui import ConverterGUI

def main():
    root = tk.Tk()
    ConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()