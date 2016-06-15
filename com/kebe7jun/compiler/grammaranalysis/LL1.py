#!/bin/env python
#coding=utf-8
__author__ = 'kebe'

class LL1:
    def __init__(self, code):
        self.code = code
        self.s_code = []
        self.first = {}
        self.fllow = {}
        self.terminal_set = set()
        self.non_terminal_set = set()
        self.find_t_or_nt_collection()

    def get_non_terminal_first(self, nt):
        for line in self.s_code:
            if nt == line['t']:
                for item in line['s']:
                    if self.is_terminal_char(item[0]):
                        self.add_terminal_to_first_collection(nt, item[0])
                    elif len(item) >= 2:
                        # if self.is_terminal_char(item[0]) and not self.is_terminal_char(item[1]):
                        #     self.add_terminal_to_first_collection(nt, item[0])
                        if not self.is_terminal_char(item[0]):
                            f = self.get_non_terminal_first(item[0])
                            for tt in f:
                                self.add_terminal_to_first_collection(nt, tt)
        return self.first[nt] if self.first.has_key(nt) else set()

    def get_first(self):
        calc_ed = []
        for item in self.non_terminal_set:
            if not item in calc_ed:
                self.get_non_terminal_first(item)
                calc_ed.append(item)
        return self.first

    def get_non_terminal_fllow(self, nt):
        for item in self.s_code:
            for it in item['s']:
                if it == '#':
                    self.add_terminal_to_fllow_collection(item['t'], it)
                if nt == it[-1]:
                    if nt != item['t']:
                        f = self.get_non_terminal_fllow(item['t'])
                        for i in f:
                            self.add_terminal_to_fllow_collection(nt, i)
                if len(it) >= 2:
                    if nt == it[-2]:
                        if self.is_terminal_char(it[-1]):
                            self.add_terminal_to_fllow_collection(nt, it[-1])
                        elif not self.is_terminal_char(it[-1]):
                            f = self.get_non_terminal_first(it[-1])
                            for i in f:
                                if i != '#':
                                    self.add_terminal_to_fllow_collection(nt, i)
                            if '#' in f:
                                f = self.get_non_terminal_fllow(it[-1])
                                for i in f:
                                    self.add_terminal_to_fllow_collection(nt, i)
        return self.fllow[nt]

    def get_fllow(self):
        self.get_first()
        s = self.s_code[0]['t']
        self.start = s
        self.add_terminal_to_fllow_collection(s, '#')
        calc_ed = []
        for item in self.non_terminal_set:
            if item not in calc_ed:
                self.get_non_terminal_fllow(item)
                calc_ed.append(item)

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
                for c in tt:
                    if self.is_terminal_char(c):
                        self.terminal_set.add(c) #Add terminal char to set

    def add_terminal_to_first_collection(self, nt, t):
        if self.first.has_key(nt):
            self.first[nt].add(t)
        else:
            self.first[nt] = set()
            self.first[nt].add(t)

    def add_terminal_to_fllow_collection(self, nt, t):
        if self.fllow.has_key(nt):
            self.fllow[nt].add(t)
        else:
            self.fllow[nt] = set()
            self.fllow[nt].add(t)

    def is_terminal_char(self, c):
        return not 'A' <= c <= 'Z'

    def get_analysis_table(self):
        t = []
        for i in self.terminal_set:
            self.first[i] = set()
            self.first[i].add(i)
        for item in self.s_code:
            for it in item['s']:
                for i in self.terminal_set:
                    if i in self.first[it[0]]:
                        t.append({
                            'nt':item['t'],
                            't':i,
                            's':'{}->{}'.format(item['t'], it)
                        })
                if '#' in self.first[it[0]]:
                    for i in self.fllow[item['t']]:
                        t.append({
                            'nt':item['t'],
                            't':i,
                            's':'{}->{}'.format(item['t'], it)
                        })
        return t

    def get_analysis_list(self, t, text):
        self.get_fllow()
        text = text + '#'
        ans = []
        read_inedx = 0
        s = []
        s.append('#')
        s.append(self.start)
        while len(s) > 0:
            x = s.pop()
            a = text[read_inedx]
            if x in self.terminal_set:
                if x == a:
                    read_inedx += 1
                else:
                    ans.append({
                        'info':'error',
                        's':self.convert_array_to_str(s),
                        'in':text[read_inedx+1::]
                    })
                    break
            else:
                if x == '#':
                    if x == a:
                        ans.append({
                            'info':'End',
                            's':self.convert_array_to_str(s),
                            'in':text[read_inedx+1::]
                        })
                        break
                    else:
                        ans.append({
                            'info':'error',
                            's':self.convert_array_to_str(s),
                            'in':text[read_inedx+1::]
                        })
                        break
                else:
                    tmp = self.is_m_x_a(t, x, a)
                    if not tmp:
                        ans.append({
                            'info':'error',
                            's':self.convert_array_to_str(s),
                            'in':text[read_inedx+1::]
                        })
                        break
                    else:
                        ttt = tmp.split('->')[1]
                        for i in range(len(ttt)):
                            s.append(ttt[-1-i])
                        ans.append({
                            'info':tmp,
                            's':self.convert_array_to_str(s),
                            'in':text[read_inedx+1::]
                        })
        return ans

    def convert_array_to_str(self, a):
        str = ''
        for i in a:
            str += i
        return str

    def is_m_x_a(self, t, x, a):
        for i in t:
            if i['nt'] == x and i['t'] == a:
                return i['s']
        return False

if __name__ == '__main__':
    ll1 = LL1('''
    E->TA
    A->+TA|#
    T->FB
    B->*FB|#
    F->(E)|i
    ''')
    ll1.get_fllow()
    print ll1.first
    print ll1.fllow
    print ll1.get_analysis_table()
    ll1.get_analysis_list(ll1.get_analysis_table(), 'i*i+i')