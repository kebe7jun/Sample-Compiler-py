#!/bin/env python
#coding=utf-8
__author__ = 'kebe'

class OperatorFirst:

    def __init__(self, code):
        self.code = code
        self.s_code = []
        self.non_terminal_set = set()
        self.terminal_set = set()
        self.f_stack = []       #To save the analysis stack
        self.l_stack = []
        self.first_vt = {}      #To save FirstVT collection
        self.last_vt = {}       #To save LastVT collection
        self.op_table = []

    def start_analysis(self):
        self.find_t_or_nt_collection()
        self.deal_first_and_last_vt()
        self.deal_operator_table()
        print self.first_vt
        print self.last_vt
        print self.op_table

    def deal_operator_table(self):
        self.s_code.insert(0, {'t':'S', 's':'#S#'})
        for p in self.s_code:
            for x in p['s']:
                for i in range(len(x)-1):
                    if self.is_terminal_char(x[i]) and self.is_terminal_char(x[i+1]): # =
                        self.op_table.append({'l':x[i], 'o':'=', 'r':x[i+1]})
                    if i< len(x) - 2 and self.is_terminal_char(x[i]) and not self.is_terminal_char(x[i+1]) and self.is_terminal_char(x[i+2]): # =
                        self.op_table.append({'l':x[i], 'o':'=', 'r':x[i+2]})
                    if self.is_terminal_char(x[i]) and not self.is_terminal_char(x[i+1]): # <
                        for t in self.first_vt[x[i+1]]:
                            self.op_table.append({'l':x[i], 'o':'<', 'r':t})
                    if not self.is_terminal_char(x[i]) and self.is_terminal_char(x[i+1]): # >
                        for t in self.last_vt[x[i]]:
                            self.op_table.append({'l':t, 'o':'>', 'r':x[i+1]})

    def deal_first_and_last_vt(self):
        while(len(self.f_stack)>0):
            item = self.f_stack.pop()
            l = self.find_P(item['t'])
            for i in l:
                if i != item['t']: # T->Tx
                    self.first_vt[i].add(item['n'])
                    self.f_stack.append({'t':i, 'n':item['n']})
        while(len(self.l_stack)>0):
            item = self.l_stack.pop()
            l = self.find_P(item['t'], True)
            for i in l:
                if i != item['t']: # T->Tx
                    self.last_vt[i].add(item['n'])
                    self.l_stack.append({'t':i, 'n':item['n']})

    def find_P(self, n, is_last_vt = False):
        l = set()
        for item in self.s_code:
            for i in item['s']:
                if i[0 if not is_last_vt else -1] == n:
                    l.add(item['t'])
        return l

    def find_t_or_nt_collection(self):
        #Find out the terminal or non terminal collection
        cs = self.code.replace(' ', '').replace('\t', '').split('\n')
        for c in cs:
            if c == '':
                continue
            cc = c.split('->')
            if len(cc) < 2:
                # Error
                continue
            t = cc[0]
            self.non_terminal_set.add(t)    #Add non terminal char to set
            t_e = cc[1]
            t_e_s = t_e.split('|')
            self.s_code.append({'t':t, 's':t_e_s})
            for tt in t_e_s:
                if self.is_terminal_char(tt[0]):
                    if not self.first_vt.has_key(t):    # If the set is none.
                        self.first_vt[t] = set()
                    self.first_vt[t].add(tt[0])
                    self.f_stack.append({'t':t, 'n':tt[0]})
                elif len(tt) > 1 and self.is_terminal_char(tt[1]):
                    if not self.first_vt.has_key(t):    # If the set is none.
                        self.first_vt[t] = set()
                    self.first_vt[t].add(tt[1])
                    self.f_stack.append({'t':t, 'n':tt[1]})
                if self.is_terminal_char(tt[-1]):
                    if not self.last_vt.has_key(t):    # If the set is none.
                        self.last_vt[t] = set()
                    self.last_vt[t].add(tt[-1])
                    self.l_stack.append({'t':t, 'n':tt[-1]})
                elif len(tt) > 1 and self.is_terminal_char(tt[-2]):
                    if not self.last_vt.has_key(t):    # If the set is none.
                        self.last_vt[t] = set()
                    self.last_vt[t].add(tt[-2])
                    self.l_stack.append({'t':t, 'n':tt[-2]})
                for c in tt:
                    self.terminal_set.add(c) #Add terminal char to set

    def is_terminal_char(self, c):
        return not 'A' <= c <= 'Z'

if __name__ == '__main__':
    of = OperatorFirst('''
        E->E+T|T
        T->T*F|F
        F->(E)|i
    ''')
    of.start_analysis()