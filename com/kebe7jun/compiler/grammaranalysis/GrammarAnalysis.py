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
			"whil":self.deal_while
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
		self.now_token_index = 0

	def start_analysis(self):
		self.analysis_line()

	def analysis_line(self):
		while not self.is_end():
			print self.get_next_token()

	def deal_program(self):
		pass

	def deal_const(self):
		pass

	def deal_var(self):
		pass

	def deal_if(self):
		pass

	def deal_for(self):
		pass

	def deal_while(self):
		pass

	def deal_repeat(self):
		pass

	#Read the next token info
	def get_next_token(self):
		try:
			t = self.token[self.now_token_index]
			self.now_token_index += 1
		except Exception:
			t = None
		return t

	#Check is analysis end.
	def is_end(self):
		return self.now_token_index >= len(self.token)