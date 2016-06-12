#coding=utf-8

from Tkinter import *

class UIMenu():
    def __init__(self, root, cmd):
        self.menu = Menu(root)
        self.parent = root
        self.cmd = cmd
        self.add_cmd()
        root['menu'] = self.menu

    def add_cmd(self):
        self.file_menu = Menu(self.menu)
        self.file_menu.add_command(label = 'Open File(Ctrl+O)', command = self.cmd.open_file)
        self.file_menu.add_command(label = 'Save File(Ctrl+S)', command = self.cmd.save_to_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Exit', command=self.cmd.exit)
        self.menu.add_cascade(label = 'File', menu = self.file_menu)

        self.menu.add_command(label = 'Words Analysis(F5)', command=self.cmd.analysis_words)
        self.menu.add_command(label = 'Grammar Analysis(F6)', command=self.cmd.analysis_grammar)
        self.menu.add_command(label = 'Generate Middle Code(F7)', command=self.cmd.generate_middle_code)
