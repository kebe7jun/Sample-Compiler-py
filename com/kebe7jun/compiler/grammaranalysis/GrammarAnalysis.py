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
			"error":"",
			"const_table":self.const_table,
			"var_table":self.var_table
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
				except Exception:
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
		is_need_deal = True
		while not self.is_end() and t['value'] not in ('var', 'begin'):
			if not is_need_deal:
				t = self.get_next_token()
				continue
			if self.is_var(t):
				tmp = {}
				tmp['name'] = t['value']
				t = self.get_next_token()
				if t['value'] != '=':
					self.write_error(t['line'], 'Unknow character {}'.format(t['value']))
					is_need_deal = False
				else:
					t = self.get_next_token()
					if self.is_const(t):
						tmp['value'] = t['value']
						tmp['type'] = t['key']
						tmp['used_times'] = 0
					else:
						self.write_error(t['line'], 'Unknow value {}'.format(t['value']))
						is_need_deal = False
					t = self.get_next_token()
					if t['value'] != ';':
						self.write_error(t['line'], 'Unexpected end for const define.')
						is_need_deal = False
					else:
						if self.is_valid_const(tmp['name']):
							self.const_table.append(tmp)
						else:
							self.write_error(t['line'], 'Already define the const name \'{}\''.format(tmp['name']))
						t = self.get_next_token()
		self.return_before_token()

	def deal_begin(self):
		print 'Analysing begin instruct...'
		t = self.get_next_token()
		while not self.is_end() and t['value'] not in ('end', 'end.'):
			if t['value'] != ';':
				try:
					func = self.module_func[t['value']]
					func()
				except Exception:
					if self.is_symbol(t):
						self.deal_instruct()
		self.return_before_token()
		pass

	def deal_var(self):
		print 'Analysing var instruct...'
		t = self.get_next_token()
		is_need_anas = True
		while t['value'] not in ('begin'):
			if not is_need_anas:
				t = self.get_next_token()
				continue
			tmp = []
			while t['value'] != ':':
				if not self.is_var(t):
					self.write_error(t['line'], 'Unexpected var name {}'.format(t['value']))
					is_need_anas = False
					break
				else:
					tmp.append({
						'name':t['value'],
						'type':'',
						'used_times':0
					})
					if not self.is_valid_const(tmp[-1]['name']):
						self.write_error(t['line'], 'Already define the name \'{}\' as a const.'.format(t['value']))
						del tmp[-1]
					elif not self.is_valid_var(tmp[-1]['name']):
						self.write_error(t['line'], 'Already define the name \'{}\' as a var.'.format(t['value']))
						del tmp[-1]
					t = self.get_next_token()
					if t['value'] == ':':
						break
					if t['value'] != ',':
						self.write_error(t['line'], 'Did not find \',\'')
						is_need_anas = False
						break
					else:
						t = self.get_next_token()
			if t['value'] == ':':
				t = self.get_next_token()
				if self.is_var_type(t):
					self.var_table.append([{'name':x['name'], 'type':t['value'], 'used_times':x['used_times']} for x in tmp])
					t = self.get_next_token()
					if t['value'] != ';':
						self.write_error(t['line'], 'Unexpect end of var define, missing \';\'')
						is_need_anas = False
					else:
						t = self.get_next_token()
				else:
					self.write_error(t['line'], 'Unexpect var type {}'.format(t['value']))
					is_need_anas = False
		self.return_before_token()

	def deal_express(self):
		t = self.get_next_token()
		dealed_list = []
		while not self.is_end() and not self.is_key_word(t):
			if self.is_var(t) or self.is_const(t):
				dealed_list.append(t)
				t = self.get_next_token()
				if not self.is_middle_symbol(t):
					# Isn't valid express
					if not self.is_key_word(t):
						self.write_error(t['line'], 'Invalid str {}.'.format(t['value']))
					while not self.is_end() and not self.is_key_word(t):
						t = self.get_next_token()
					self.return_before_token()
					break
				dealed_list.append(t)
				t = self.get_next_token()
				# if t['value'] in ('(', ')'):
				# 	type = self.deal_bracket()
			elif t['value'] in ('(', ')'):
				type = self.deal_bracket()
			elif t['value'] in ('+', '-'):
				t = self.get_next_token()
				if not self.is_const(t) or not self.is_var(t):
					# Isn't valid express
					if not self.is_key_word(t):
						self.write_error(t['line'], 'Invalid str {}.'.format(t['value']))
					while not self.is_end() and not self.is_key_word(t):
						t = self.get_next_token()
					self.return_before_token()
					break

		print dealed_list
		pass

	def deal_bracket(self):
		t = self.get_next_token()
		while t['value'] != ')':
			if t['value'] == '(':
				self.deal_bracket()
			t = self.get_next_token()
		pass

	def deal_if(self): 
		'''
			Here set the priority that
			( + - * / ) > (and or not) > (> < >= <= <>)
		'''
		self.deal_express()
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

	def is_key_word(self, t):
		return t['key'] <= 20

	def is_symbol(self, t):
		return t['key'] == 34

	def is_relation_symbol(self, t):
		return 28 <= t['key'] <= 33

	def is_logic_symbol(self, t):
		return 21 <= t['key'] <= 23

	def is_calc_symbol(self, t):
		return 24 <= t['key'] <= 27

	def is_var(self, t):
		return t['key'] == 34

	def is_const(self, t):
		return 35 <= t['key'] <= 38

	def is_var_type(self, t):
		return 3<=t['key'] <=6

	def is_middle_symbol(self, t):
		return 22<=t['key'] <=33

	def write_error(self, line, err):
		self.result['error'] += 'Line {}: {}\n'.format(line, err)
		print err

	def is_valid_const(self, c):
		return not [x for x in self.const_table if x['name'] == c]

	def is_valid_var(self, c):
		return not [x for x in self.var_table if x['name'] == c]

	def is_middle_symbol(self, t):
		return 22<=t['key'] <=33