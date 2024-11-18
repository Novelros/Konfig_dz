import tkinter as tk
from start import ShellEmulator
from tar1 import VirtualFileSystem

class ShellGUI:
    def __init__(self, shell):
        self.shell = shell
        self.root = tk.Tk()
        self.root.title("Shell Emulator")

        self.text_output = tk.Text(self.root)
        self.text_output.pack()

        self.entry_input = tk.Entry(self.root)
        self.entry_input.pack()
        self.entry_input.bind("<Return>", self.process_command)

    def process_command(self, event):
        command = self.entry_input.get()
        self.entry_input.delete(0, tk.END)
        self.text_output.insert(tk.END, f"{self.shell.prompt()}{command}\n")
        output = self.shell.execute_command(command)
        if output:
            self.text_output.insert(tk.END, f"{output}\n")

    def start(self):
        self.root.mainloop()

    def change_text_style(self, font_size, font_style):
        self.text_output.config(font=(font_style, font_size))

    def change_background_color(self, color):
        self.text_output.config(bg=color)

def run_gui(username, fs, fs_tar ,start_script):
    shell = ShellEmulator(username, fs , fs_tar)
    shell.execute_commands_from_file(start_script)
    gui = ShellGUI(shell)
    gui.change_text_style(12, "Arial")  # Шрифт Arial размером 13
    gui.change_background_color("lightgray")  # Серый цвет фона
    gui.start()



