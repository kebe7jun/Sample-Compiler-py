#!/bin/env python
#coding=utf-8
__author__ = 'kebe'
from Tkinter import *

def get_text_content(text):
    return text.get(0.0, END)[0:-1]

def set_text_content(text, content):
    text.delete(0.0, END)
    text.insert(1.0, content)

def trans_obj_to_table(data, title, type = 1):
    out = title + ':\n'
    out += '%5s' % ''
    cols = [x for x in data['cols']]
    rows = [x for x in data['rows']]
    for i in range(len(cols)):
        out += '|%5s' % cols[i]
    out += '\n'
    for i in range(len(cols)):
        out+='-----|'
    out+='-----'
    out += '\n'
    for i in range(len(rows)):
        out += '%5s' % rows[i]
        for j in range(len(cols)):
            out += '|%5s' % get_content_by_row_and_col(data['data'], rows[i], cols[j], type)
        out += '\n'
    return out

def get_content_by_row_and_col(data, r, c, type):
    if type == 1:
        try:
            f = data[r]
            for i in f:
                if i == c:
                    return 1
        except Exception:
            pass
        return ''
    elif type == 2:
        for i in data:
            if r == i['r'] and c == i['c']:
                return i['v']
        return ''