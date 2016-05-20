#coding=utf-8

import re
import time
import random

class WordsAnalysis:

    token_table = {
        "program":1,
        "var":2,
        "integer":3,
        "bool":4,
        "real":5,
        "char":6,
        "const":7,
        "begin":8,
        "if":9,
        "then":10,
        "else":11,
        "while":12,
        "do":13,
        "for":14,
        "to":15,
        "end":16,
        "read":17,
        "write":18,
        "true":19,
        "false":20,
        "not":21,
        "and":22,
        "or":23,
        "+":24,
        "-":25,
        "*":26,
        "/":27,
        "<":28,
        ">":29,
        "<=":30,
        ">=":31,
        "==":32,
        "<>":33,
        "=":39,
        ";":40,
        ",":41,
        "\'":42,
        "/*":43,
        "*/":44,
        ":":45,
        "(":46,
        ")":47,
        ".":48,
        "end.":0,
    }

    def __init__(self, code):
        self.code = code
        self.value = {}

    def start_analysis(self):
        msg = self.find_not_support_char()
        if msg != '':
            return {
                'info':'',
                'error':msg
            }
        return self.split_code_to_world()

    def check_valid_character(self):
        p = re.compile('[A-Za-z0-9;\\.\\+\\-\\*/<>=!:\\(\\)\\\' \\n\\r\\t]+')    # Support characters
        m = p.match(self.code)
        return m is not None

    def find_not_support_char(self):
        strs = self.code.split('\n')
        msg = ''
        i = 1

        for item in strs:
            j = 0
            count_of_semicolon = 0
            for c in item:
                j += 1
                if c == '\'':
                    count_of_semicolon += 1
                if count_of_semicolon%2 == 1:    #Don't explame the content in ''
                    continue
                if c not in '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM<>:= \t"\';,./+-*()':
                    msg += 'Line {0} error({1}): Unexcepted character \'{2}\'\n'.format(i, j, c)
            i += 1
        return msg

    def split_code_to_world(self):
        self.value = {}
        self.code = self.convert_str_to_value(self.code)
        self.code = self.delete_note(self.code)
        self.code = self.code.replace('\t', ' ')
        strs = self.code.split('\n')
        error = ''
        token = []
        line = 1
        for item in strs:
            s = self.add_blank_to_code(item)
            s = s.split(' ')
            i = 0
            for i in range(len(s)):
                try:
                    item = s[i]
                except Exception as e:
                    continue
                item = str(item)
                e = ''
                if item == '':
                    continue
                try:
                    k = self.token_table[item]
                except KeyError:
                    if item == 'true' or item == 'false':
                        k=38
                    elif item[0] == '_':
                        k=37
                        item = self.value[item]
                    # elif '.' in item:
                    #     try:
                    #         float(item)
                    #         k=36
                    #     except Exception:
                    #         e = 'Line {} error: Unexpected word "{}"\n'.format(line, item)
                    elif item[0] in '1234567890-+':
                        isFloat = True if '.' in item else False
                        k = 36 if isFloat else 35
                        # print item
                        try:
                            p = re.compile('^[0-9]+(\\.[0-9]+)?[eE][0-9]?')
                            if p.match(item):
                                try:
                                    nitem = s[i+1]
                                    print nitem
                                    if nitem == '+' or nitem == '-':
                                        try:
                                            int(s[i+2])
                                            item = item + nitem + s[i+2]
                                            del s[i+1]
                                            del s[i+1]
                                        except Exception:
                                            pass
                                except Exception:
                                    pass
                            else:
                                float(item)
                        except Exception:
                            e = 'Line {} error: Unexpected word "{}"\n'.format(line, item)
                    else:
                        p = re.compile('^[a-zA-Z][a-zA-Z0-9]?')
                        if p.match(item):
                            k=34
                        else:
                            e = 'Line {} error: Unexpected word "{}"\n'.format(line, item)
                if e == '':
                    token.append({"line":line, "key":k, "value":item})
                else:
                    error += e
            line += 1
        # print token
        # print token
        return {
            'error':error,
            'token':token
        }

    def add_blank_to_code(self, str):
        #Add blank to the source code

        s = ''
        for i in range(len(str)):
            try:
                if str[i] in '+-()*/,:;':
                    s += ' {} '.format(str[i])
                elif str[i] in '<>=':
                        if str[i+1] == '=' or (str[i] == '<' and str[i+1] == '>'):
                            s += ' {}{} '.format(str[i], str[i+1])
                            i += 1
                        else:
                            s += ' {} '.format(str[i])
                # elif str[i] in '+-':
                #     if str[i+1] in '0123456789':    #is number
                #         s += ' {}'.format(str[i])
                #     else:
                #         s += ' {} '.format(str[i])
                else:
                    s += str[i]
            except Exception:
                s += ' {}'.format(str[i])
        # print s
        return s

    def convert_str_to_value(self, code):
        strs = code.split('\n')
        code = ''
        c = ''
        for str in strs:
            s = ''
            count_of_semicolon = 0
            v = ''
            for i in range(len(str)):
                c = str[i]
                if str[i] == '\'':
                    count_of_semicolon += 1
                    if v != '' and count_of_semicolon%2 == 0:
                        key = '_str_{}'.format(time.time() + random.random())
                        self.value[key] = v[1::]
                        s += ' {} '.format(key)
                        v = ''
                        c = ''
                if count_of_semicolon%2 == 1:    #Don't explame the content in ''
                    v += str[i]
                    continue
                s += c
            if v != '':
                s+=v
            code += s + '\n'
        return code

    def delete_note(self, code):
        code = self.delete_note_lines(code)
        strs = code.split('\n')
        code = ''
        for str in strs:
            code += re.sub('//[\\d\\D]*', '', str) +'\n'
        return code

    def delete_note_lines(self, code):
        is_in_note = False
        cc = ''
        is_pass_one = False
        for i in range(len(code)):
            if is_pass_one:
                is_pass_one = False
                continue
            # print code[i:i+2]
            if code[i:i+2] == '/*' and not is_in_note:
                is_pass_one = True
                is_in_note = True
            if is_in_note and code[i] == '\n':
                cc+=code[i]
            if not is_in_note:
                cc+=code[i]
            if code[i:i+2] == '*/' and is_in_note:
                is_pass_one = True
                is_in_note = False
        return cc
