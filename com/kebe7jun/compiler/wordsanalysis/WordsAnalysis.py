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
        info = ''
        error = ''
        token = []
        line = 1
        for item in strs:
            s = self.add_blank_to_code(item)
            s = s.split(' ')
            for item in s:
                item = str(item)
                if item == '':
                    continue
                try:
                    k = self.token_table[item]
                    info += '{}: ({}, "{}")\n'.format(line, k, item)
                    token.append((k, item))
                except KeyError:
                    if item == 'true' or item == 'false':
                        k=38
                        info += '{}: ({}, "{}")\n'.format(line, k, item)
                        token.append((k, item))
                    elif item[0] == '_':
                        k=37
                        info += '{}: ({}, "{}")\n'.format(line, k, self.value[item])
                        token.append((k, item[1:-1]))
                    elif item[0] == '\'' and item[-1] == '\'':
                        k=37
                        info += '{}: ({}, "{}")\n'.format(line, k, item[1:-1])
                        token.append((k, item[1:-1]))
                    elif '.' in item:
                        try:
                            float(item)
                            k=36
                            info += '{}: ({}, "{}")\n'.format(line, k, item)
                            token.append((k, item))
                        except Exception:
                            error += 'Line {} error: Unexpected word "{}"\n'.format(line, item)
                    elif item[0] in '1234567890-+':
                        try:
                            int(item)
                            k=35
                            info += '{}: ({}, "{}")\n'.format(line, k, item)
                            token.append((k, item))
                        except Exception:
                            error += 'Line {} error: Unexpected word "{}"\n'.format(line, item)
                    else:
                        p = re.compile('^[a-zA-Z][a-zA-Z0-9]?')
                        if p.match(item):
                            k=34
                            info += '{}: ({}, "{}")\n'.format(line, k, item)
                            token.append((k, item))
                        else:
                            error += 'Line {} error: Unexpected word "{}"\n'.format(line, item)
            line += 1
        print token
        return {
            'info':info,
            'error':error,
            'token':token
        }

    def add_blank_to_code(self, str):
        #Add blank to the source code

        s = ''
        for i in range(len(str)):
            try:
                if str[i] in '()*/,:;':
                    s += ' {} '.format(str[i])
                elif str[i] in '<>=':
                        if str[i+1] == '=' or (str[i] == '<' and str[i+1] == '>'):
                            s += ' {}{} '.format(str[i], str[i+1])
                            i += 1
                elif str[i] in '+-':
                    if str[i+1] in '0123456789':    #is number
                        s += ' {}'.format(str[i])
                    else:
                        s += ' {} '.format(str[i])
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
        # r = re.compile('/\\*[\\d\\D]*\\*/')
        # p = r.findall(code)
        # print p
        # for item in p:
        #     t = len(item.split('\n'))
        #     ns = ''
        #     for i in range(t):
        #         ns += '\n'
        #     code = code.replace(item, ns)
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
            print code[i:i+2]
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