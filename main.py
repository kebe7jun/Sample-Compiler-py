#coding=utf-8
import com.kebe7jun.compiler.ui.MainFrame
import com.kebe7jun.compiler.ui.OperatorFirstFrame
from Tkinter import *
import com.kebe7jun.compiler.cmd.MenuAction

root = Tk()
cmd = com.kebe7jun.compiler.cmd.MenuAction.Cmd()
# frame = com.kebe7jun.compiler.ui.MainFrame.MainFrame(root, cmd)
frame = com.kebe7jun.compiler.ui.OperatorFirstFrame.OperatorFirstFrame(root)
cmd.set_frame(frame)
root.mainloop()
