#!/bin/env python
#coding=utf-8
from com.kebe7jun.compiler.wordsanalysis.WordsAnalysis import *

class GrammarAnalysis():
	"""
		To analysis the grammar of sample language.
	"""
	def __init__(self, token = None, code = None):
		# print type(token)

		#The to deal module functions table
		self.module_func = {
			"if":self.deal_if,
			"for":self.deal_for,
			"repeat":self.deal_repeat,
			"whil":self.deal_while,
			"const":self.deal_const,
			"var":self.deal_var,
			"begin":self.deal_begin
		}
		#Check wether to run word analysis
		if token is None:
			if code is None:
				print 'Please enter code or token table.'
			else:
				# Do word analysis
				wa = WordsAnalysis(code)
				res = wa.start_analysis()
				self.token = res['token']
		else:
			self.token = token
		self.const_table = []
		self.var_table = []
		self.now_token_index = 0
		self.result = {
			"result":"",
			"error":""
		}

	def start_analysis(self):
		self.analysis_line()
		if not self.deal_program():
			self.result['error'] = 'Can\'t find the enterance of the program.\n'
		while not self.is_end():
			t = self.get_next_token()
			if t['value'] != ';':
				try:
					func = self.module_func[t['value']]
					func()
				except Exception, e:
					if self.is_symbol(t):
						self.deal_instruct()

		return self.result

	def analysis_line(self):
		pass

	def deal_program(self):
		return self.get_next_token()['key'] == 1 and self.is_symbol(self.get_next_token())

	def deal_const(self):
		print 'Analysing const instruct...'
		t = self.get_next_token()
		while t['value'] not in ('var', 'begin'):
			t = self.get_next_token()
		self.return_before_token()

	def deal_begin(self):
		print 'Analysing begin instruct...'
		t = self.get_next_token()
		while t['value'] not in ('end', 'end.'):
			t = self.get_next_token()
		self.return_before_token()
		pass

	def deal_var(self):
		print 'Analysing var instruct...'
		t = self.get_next_token()
		while t['value'] not in ('begin'):
			t = self.get_next_token()
		self.return_before_token()

	def deal_if(self): 
		'''
			Here set the priority that
			( + - * / ) > (and or not) > (> < >= <= <>)
		'''
		pass

	def deal_for(self):
		pass

	def deal_while(self):
		pass

	def deal_repeat(self):
		pass

	def deal_instruct(self):
		pass

	#Read the next token info
	def get_next_token(self):
		try:
			t = self.token[self.now_token_index]
			self.now_token_index += 1
		except Exception:
			t = None
		return t

	def return_before_token(self):
		self.now_token_index -= 1

	#Check is analysis end.
	def is_end(self):
		return self.now_token_index >= len(self.token)

	def is_symbol(self, t):
		return t['key'] == 34

	def is_relation_symbol(self, t):
		return 28 <= t['key'] <= 33

	def is_logic_symbol(self, t):
		return 21 <= t[key] <= 23

	def is_calc_symbol(self, t):
		return 24 <= t[key] <= 27