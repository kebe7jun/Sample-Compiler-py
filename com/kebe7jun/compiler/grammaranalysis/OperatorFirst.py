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
        self.start = ''

    def start_analysis(self):
        self.find_t_or_nt_collection()
        self.deal_first_and_last_vt()
        self.deal_operator_table()
        return {
            'f':self.first_vt,
            'l':self.last_vt,
            'op':self.op_table,
            't':self.terminal_set,
            'nt':self.non_terminal_set
        }

    def deal_operator_table(self):
        self.s_code.insert(0, {'t':self.start, 's':['#'+self.start+'#']})
        self.terminal_set.add('#')
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
            if self.start == '':
                self.start = t
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
                    if self.is_terminal_char(c):
                        self.terminal_set.add(c) #Add terminal char to set

    def is_terminal_char(self, c):
        return not 'A' <= c <= 'Z'

    def get_analysis_table(self, text):
        text += '#'
        top = 0
        s = []
        s.append('#')
        p_table = []
        read_index = 0
        p_table.append({
                    's':self.convert_array_to_str(s),
                    'in':text,
                    'info':'Init'
                })
        try:
            while read_index < len(text):
                a = text[read_index]
                j = 0
                if a != '#' and a not in self.terminal_set:
                    p_table.append({
                        's':self.convert_array_to_str(s),
                        'in':text[read_index+1::],
                        'info':'Error, unexpected char ' + a
                    })
                    break
                if self.is_terminal_char(s[top]):
                    j = top
                else:
                    j = top-1
                tmp = self.get_op_l_and_r(s[j], a)
                if tmp == '<' or tmp == '=':
                    top += 1
                    if len(s) <= top:
                        s.append(a)
                    else:
                        s[top] = a
                    p_table.append({
                        's':self.convert_array_to_str(s),
                        'in':text[read_index+1::],
                        'info':a + ' in stack'
                    })
                    read_index += 1
                if tmp == '>':
                    q = s[j]
                    while True:
                        q = j
                        if self.is_terminal_char(s[j-1]):
                            j = j -1
                        else:
                            j = j-2
                        tmp = self.get_op_l_and_r(s[j], s[q])
                        if tmp == '<':
                            break
                    str1 = s[j+1:top+1]
                    str = self.find_nt_by_str(str1)
                    p_table.append({
                        's':self.convert_array_to_str(s),
                        'in':text[read_index+1::],
                        'info':self.convert_array_to_str(str1) + '->' + str
                    })
                    top = j+1
                    s[top] = str
                if s[0] == '#' and s[1] == self.start and a == '#':
                    break
        except Exception:
            pass
        return p_table

    def find_nt_by_str(self, str):
        str = self.convert_array_to_str(str)
        s = ''
        times = 0
        nts = 0
        for i in str:
            if not self.is_terminal_char(i):
                nts += 1
        for item in self.s_code:
            for it in item['s']:
                if self.is_like(it, str):
                    times = 0
                    for i in range(len(it)):
                        if not self.is_terminal_char(it[i]) and self.can_from_l_to_r(it[i], str[i]):
                            times += 1
                    if times == nts:
                        return item['t']


    def is_like(self, s1, s2):
        if len(s1) != len(s2):
            return False
        for i in range(len(s1)):
            if self.is_terminal_char(s1[i]) != self.is_terminal_char(s2[i]):
                return False
            if self.is_terminal_char(s1[i]) and self.is_terminal_char(s2[i]):
                if s1[i] != s2[i]:
                    return False
        return True

    def can_from_l_to_r(self, l, r):
        if l == r:
            return True
        for item in self.s_code:
            for it in item['s']:
                if l == item['t'] and len(it) == 1 and not self.is_terminal_char(it[0]):
                    return self.can_from_l_to_r(it, r)
        return False

    def get_op_l_and_r(self, l, r):
        for i in self.op_table:
            if i['l'] == l and i['r'] == r:
                return i['o']
        return None

    def convert_array_to_str(self, a):
        str = ''
        for i in a:
            str += i
        return str


if __name__ == '__main__':
    of = OperatorFirst('''
        E->E+T|T
        T->T*F|F
        F->(E)|i
    ''')
    of.start_analysis()
    print of.get_analysis_table('i+i+')