#coding=utf-8
import ui.MainFrame
from Tkinter import *
import com.kebe7jun.compiler.cmd.MenuAction

root = Tk()
cmd = com.kebe7jun.compiler.cmd.MenuAction.Cmd()
frame = ui.MainFrame.MainFrame(root, cmd)
cmd.set_frame(frame)
root.mainloop()