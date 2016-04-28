#coding=utf-8

from Tkinter import *
import UIMenu
import NumberText
class MainFrame(Frame):
    def __init__(self, root, command):
        Frame.__init__(self, master=root)
        self.root = root
        self.cmd = command
        self.ui_menu = UIMenu.UIMenu(root, command)
        self.config(width = 800, height = 500)
        self.pack()
        self.edit_text = NumberText.NumberText(self, height=1000)
        self.edit_text.grid(row = 0, column = 0)
        self.edit_text = self.edit_text.text
        self.right_frame = Frame(self)
        self.right_frame.grid(row = 0, column = 1)
        self.edit_text_show = NumberText.NumberText(self.right_frame)
        self.edit_text_show.grid(row = 0, column = 0)
        self.edit_text_show = self.edit_text_show.text
        self.edit_text_msg = NumberText.NumberText(self.right_frame)
        self.edit_text_msg.grid(row = 1, column = 0)
        self.edit_text_msg = self.edit_text_msg.text
        self.bind_envent()

    def bind_envent(self):
        self.edit_text.bind('<Control-Key-s>', self.cmd.save_to_file)
        self.edit_text.bind('<Control-Key-S>', self.cmd.save_to_file)
        self.edit_text.bind('<Control-Key-a>', self.select_text)
        self.edit_text.bind('<Control-Key-o>', self.cmd.open_file)
        self.edit_text.bind('<F5>', self.cmd.analysis_words)
        # self.edit_text_show.bind('<Button-1>', self.select_texttext)
        self.edit_text_show.bind('<Button-1>', self.cmd.on_text_show_line_select)
        self.edit_text_msg.bind('<Button-1>', self.cmd.on_text_msg_line_select)

    def select_text(self, e):
        self.edit_text.tag_add(SEL, 1.0, END)
        return 'break'