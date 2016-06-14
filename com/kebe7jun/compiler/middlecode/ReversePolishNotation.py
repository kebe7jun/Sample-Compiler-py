#!/bin/env python
#coding=utf-8
__author__ = 'kebe'

class ReversePolishNotation:

    def __init__(self, expr):
        self.expr = expr
        self.pro = {
            '#':0,
            '<=':1,
            '>=':1,
            '==':1,
            '<>':1,
            '<':1,
            '>':1,
            '+':2,
            '-':2,
            '*':3,
            '/':3,
            'or':4,
            'and':4,
            'not':4,
        }

    def getPlishNotation(self):
        s1 = []
        s2 = []
        s1.append({'value':'#'})
        for x in self.expr:
            if x['value'] == '(':
                s1.append(x)
            elif x['value'] == ')':
                while s1[-1]['value'] != '(':
                    s2.append(s1.pop())
                s1.pop()
            elif x['value'] in ('+', '-', '*', '/', '<', '>', '>=', '<=', '==', '<>', 'or', 'and', 'not'):
                if s1[-1]['value'] == '(':
                    s1.append(x)
                elif self.pro[x['value']] > self.pro[s1[-1]['value']]:
                    s1.append(x)
                else:
                    while self.pro[s1[-1]['value']] >= self.pro[x['value']] and s2[-1] != '(':
                        s2.append(s1.pop())
                    s1.append(x)
            else:
                s2.append(x)

        while s1[-1]['value'] != '#':
            s2.append(s1.pop())

        return s2
