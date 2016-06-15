#coding=utf-8

from Tkinter import *

import tkFileDialog
from com.kebe7jun.compiler.wordsanalysis.WordsAnalysis import *
from com.kebe7jun.compiler.grammaranalysis.GrammarAnalysis import *
from com.kebe7jun.compiler.middlecode.GeneMiddleCode import *
from com.kebe7jun.compiler.ui.OperatorFirstFrame import *
from com.kebe7jun.compiler.ui.MainFrame import *
import time


class Cmd:
    def set_frame(self, frame):
        self.frame = frame
        self.filename = ''
        self.last_click_text_show_time = 0

    def open_file(self, e = None):
        print 'Opening file...'
        self.filename = tkFileDialog.askopenfilename()
        if self.filename != '':
            print self.filename + ' opened'
            self.frame.edit_text.delete(0.0, END)
            self.frame.edit_text.insert(1.0, open(self.filename).read())
            pass

    def analysis_grammar(self, e = None):
        wa = WordsAnalysis(self.get_content())
        res = wa.start_analysis()
        if res['error'] != '':
            info = ''
            for item in res['token']:
                info += '{}:\t{}\t\t{}\n'.format(item['line'], item['key'], item['value'])
            self.set_edit_text_msg_content(res['error'])
            self.set_edit_text_show_content(info)
            return
        else:
            ga = GrammarAnalysis(code = self.get_content())
            res = ga.start_analysis()
            self.set_edit_text_msg_content(res['error'])
            self.set_edit_text_show_content(res['result'])

    def generate_middle_code(self, e = None):
        ga = GrammarAnalysis(code = self.get_content())
        res = ga.start_analysis()
        if res['error'] != '':
            self.set_edit_text_msg_content(res['error'])
            self.set_edit_text_show_content(res['result'])
            return
        else:
            ga = GenerateMiddleCode(code = self.get_content())
            res = ga.start_analysis()
            mid = res['mid']
            r = ''
            for i in range(len(mid)):
                r += '%3d: (%-4s %-5s %-5s %-5s)\n' % (i + 1, mid[i][0], mid[i][1], mid[i][2], mid[i][3])
            self.set_edit_text_msg_content(res['error'])
            self.set_edit_text_show_content(r)

    #words analysis
    def analysis_words(self, e = None):
        wa = WordsAnalysis(self.get_content())
        res = wa.start_analysis()
        info = ''
        for item in res['token']:
            info += '{}:\t{}\t\t{}\n'.format(item['line'], item['key'], item['value'])
            self.set_edit_text_msg_content(res['error'])
            self.set_edit_text_show_content(info)

    def set_edit_text_show_content(self, content):
        self.frame.edit_text_show.delete(0.0, END)
        self.frame.edit_text_show.insert(1.0, content)

    def set_edit_text_msg_content(self, content):
        self.frame.edit_text_msg.delete(0.0, END)
        self.frame.edit_text_msg.insert(1.0, content)

    def save_to_file(self, e = None):
        if(self.filename != ''):
            print 'Save file to '+self.filename
            f = open(self.filename, 'w')
            f.write(self.get_content())
            f.close()
        else:   #No open file
            fn = tkFileDialog.asksaveasfilename()
            f = open(fn, 'w')
            f.write(self.get_content())
            self.filename = fn

    def open_of(self, e = None):
        root = Tk()
        OperatorFirstFrame(root)
        root.mainloop()

    def get_content(self):
        return self.frame.edit_text.get(0.0, END)[0:-1]

    def on_text_show_line_select(self, e = None):
        if time.time() - self.last_click_text_show_time < 0.5:
            line = self.frame.edit_text_show.index(INSERT).split('.')[0]
            content = self.frame.edit_text_show.get(float(line), float(line)+0.999)
            sline = int(content.split(':')[0])
            self.select_line(sline)
            return 'break'
        else:
            self.last_click_text_show_time = time.time()

    def on_text_msg_line_select(self, e = None):
        if time.time() - self.last_click_text_show_time < 0.5:
            line = self.frame.edit_text_msg.index(INSERT).split('.')[0]
            content = self.frame.edit_text_msg.get(float(line), float(line)+0.999)
            sline = int(content.split(' ')[1])
            self.select_line(sline)
            return 'break'
        else:
            self.last_click_text_show_time = time.time()

    def select_line(self, line):
        try:
            self.frame.edit_text.tag_delete(SEL)
        except Exception:
            pass
        self.frame.edit_text.tag_add(SEL, float(line), float(line)+0.999)

    def exit(self, e = None):
        exit(0)
