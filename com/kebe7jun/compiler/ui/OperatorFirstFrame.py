#!/bin/env python
#coding=utf-8
__author__ = 'kebe'

from Tkinter import *
from com.kebe7jun.compiler.grammaranalysis.OperatorFirst import *
from com.kebe7jun.compiler.tools.Tools import *

class OperatorFirstFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, master=root)
        self.config(width = 800, height = 500)
        self.pack()
        self.input_text = Text(self)
        self.input_text.config(width = 60, height = 10)
        self.input_text.grid(row = 0, column = 0)
        self.sure_btn = Button(self, text = 'Start analysis')
        self.sure_btn.config(width = 20, height = 1)
        self.sure_btn.grid(row = 1, column = 0)
        self.first_vt_show = Text(self)
        self.first_vt_show.config(width = 60, height = 10)
        self.first_vt_show.grid(row = 2, column = 0)
        self.last_vt_show = Text(self)
        self.last_vt_show.config(width = 60, height = 10)
        self.last_vt_show.grid(row = 3, column = 0)

        self.table_show = Text(self)
        self.table_show.config(width = 60, height = 10)
        self.table_show.grid(row = 0, column = 1)
        self.input_text_1 = Text(self)
        self.input_text_1.config(width = 60, height = 1)
        self.input_text_1.grid(row = 1, column = 1)
        self.analysis_show = Text(self)
        self.analysis_show.config(width = 60, height = 20)
        self.analysis_show.grid(row = 2, column = 1, rowspan = 2)
        self.bind_event()

    def bind_event(self):
        set_text_content(self.input_text, '''
        E->E+T|T
        T->T*F|F
        F->(E)|i
        ''')
        self.sure_btn.bind('<Button-1>', self.show)

    def show(self, e = None):
        op = OperatorFirst(get_text_content(self.input_text))
        res = op.start_analysis()
        set_text_content(self.first_vt_show, trans_obj_to_table(self.get_format_data_first(res), 'FirstVT'))
        set_text_content(self.last_vt_show, trans_obj_to_table(self.get_format_data_last(res), 'LastVT'))
        set_text_content(self.table_show, trans_obj_to_table(self.get_format_data_table(res), 'Relation Table', 2))

    def get_format_data_first(self, data):
        rows = data['nt']
        cols = data['t']
        data = data['f']
        return {
            'rows':rows,
            'cols':cols,
            'data':data
        }

    def get_format_data_last(self, data):
        rows = data['nt']
        cols = data['t']
        data = data['l']
        return {
            'rows':rows,
            'cols':cols,
            'data':data
        }

    def get_format_data_table(self, data):
        rows = data['t']
        cols = data['t']
        data = [{'r':x['l'], 'c':x['r'], 'v':x['o']} for x in data['op']]
        return {
            'rows':rows,
            'cols':cols,
            'data':data
        }
