#coding=utf-8
import com.kebe7jun.compiler.ui.MainFrame
from Tkinter import *
import com.kebe7jun.compiler.cmd.MenuAction

root = Tk()
cmd = com.kebe7jun.compiler.cmd.MenuAction.Cmd()
frame = com.kebe7jun.compiler.ui.MainFrame.MainFrame(root, cmd)
cmd.set_frame(frame)
root.mainloop()