#!/bin/env python
#coding=utf-8

from com.kebe7jun.compiler.wordsanalysis.WordsAnalysis import *
from ReversePolishNotation import *

class GenerateMiddleCode:
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
			"while":self.deal_while,
			"const":self.deal_const,
			"var":self.deal_var,
			"begin":self.deal_begin
		}
		self.t_index = 1
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
			"mid":[],
			"const_table":self.const_table,
			"var_table":self.var_table
		}

	def start_analysis(self):
		self.out_index = 4
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
		self.print_middle_code('', '', '', '')
		# self.do_last_work()
		return self.result

	def do_last_work(self):
		mid = self.result['mid']
		j = 0
		for i in range(len(mid)):
			i = i-j
			if mid[i][0] in ('<', '>', '<=', '>=', '==', '<>'):
				j += 1
				mid[i + 1][0] = 'j' + mid[i][0]
				mid[i + 1][1] = mid[i][1]
				mid[i + 1][2] = mid[i][2]
				del mid[i]
				for item in mid:
					try:
						a = int(item[3])
						if a > i:
							item[3] = str(a-1)
					except Exception:
						pass

	def print_info(self, w):
		for i in range(self.out_index):
			self.result['result'] += ' '
		self.result['result'] += w + '\n'

	def analysis_line(self):
		pass

	def deal_program(self):
		self.print_info('Analysis the program head.')
		r = self.get_next_token()['key'] == 1 and self.is_symbol(self.get_next_token())
		self.print_info('Analysis the program head done.')
		return r

	def deal_const(self):
		print 'Analysing const instruct...'
		self.print_info('Analysing const area...')
		t = self.get_next_token()
		is_need_deal = True
		self.out_index += 4
		while not self.is_end() and t['value'] not in ('var', 'begin'):
			if not is_need_deal:
				t = self.get_next_token()
				continue
			if self.is_var(t):
				self.print_info('Analysing const...')
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
		self.out_index -=4
		self.print_info('Const area analysis done.')

	def deal_begin(self):
		print 'Analysing begin instruct...'
		self.print_info('Analysing start part...')
		t = self.get_next_token()
		self.out_index += 4
		while not self.is_end() and t['value'] not in ('end', 'end.'):
			if t['value'] != ';':
				try:
					self.module_func[t['value']]()
				except Exception:
					if self.is_symbol(t):
						self.return_before_token()
						self.deal_instruct()
			t = self.get_next_token()
		self.out_index -=4
		if t['value'] in ('end', 'end.'):
			self.print_info('Start part analysis done.')
		self.return_before_token()


	def deal_var(self):
		print 'Analysing var instruct...'
		self.print_info('Analysing var area...')
		t = self.get_next_token()
		is_need_anas = True
		self.out_index += 4
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
					try:
						if not self.is_valid_const(tmp[-1]['name']):
							self.write_error(t['line'], 'Already define the name \'{}\' as a const.'.format(t['value']))
							del tmp[-1]
						elif not self.is_valid_var(tmp[-1]['name']):
							self.write_error(t['line'], 'Already define the name \'{}\' as a var.'.format(t['value']))
							del tmp[-1]
					except Exception,e:
						pass
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
					self.print_info('Analysing {} type var...'.format(t['value']))
					([self.var_table.append({'name':x['name'], 'type':t['value'], 'used_times':x['used_times']}) for x in tmp])
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
		self.out_index -= 4
		self.print_info('Var area analysis done.')

	def gene_middle_code(self, expr):
		s = 0
		e = []
		c = []
		for i in range(len(expr)):
			if expr[i]['value'] in ('not', 'and', 'or'):
				r = ReversePolishNotation(expr[s:i])
				e.append(expr[s:i])
				s = i+1
				c.append(expr[i])
		e.append(expr[s:len(expr)])
		for i in range(len(e)):
			r = ReversePolishNotation(e[i])
			e[i] = r.getPlishNotation()
		c.reverse()
		return {'e':e, 'c':c}

	def deal_express(self, is_in_b = False):
		start_index = self.now_token_index
 		t = self.get_next_token()
		dealed_list = []
		self.print_info('Analysing express...')
		while not self.is_end() and not self.is_key_word(t):
			if self.is_var(t) or self.is_const(t):
				if self.is_var(t):
					if  self.is_valid_var(t['value']) and self.is_valid_const(t['value']):
						self.write_error(t['line'], 'Undefined var \'{}\''.format(t['value']))
				dealed_list.append(t)
				t = self.get_next_token()
				if t['value'] == ')' and is_in_b:
					self.return_before_token()
					return
				if not self.is_middle_symbol(t):
					# Isn't valid express
					# if not self.is_key_word(t):
					# 	self.write_error(t['line'], 'Invalid str \'{}\'.'.format(t['value']))
					self.return_before_token()
					self.read_to_instruct_end()
					break
				dealed_list.append(t)
				t = self.get_next_token()
				# if t['value'] in ('(', ')'):
				# 	type = self.deal_bracket()
			elif t['value'] in ('(', ')'):
				type = self.deal_bracket()
				t = self.get_next_token()
				if not self.is_middle_symbol(t):
					# Isn't valid express
					# if not self.is_key_word(t) or t['value'] != ';':
					# 	self.write_error(t['line'], 'Invalid str \'{}\'.'.format(t['value']))
					# while not self.is_end() and not self.is_key_word(t):
					# 	t = self.get_next_token()
					self.return_before_token()
					break
				dealed_list.append(t)
				t = self.get_next_token()
				# t = self.get_next_token()
			elif t['value'] in ('+', '-'):
				t = self.get_next_token()
				if not self.is_const(t) and not self.is_var(t):
					# Isn't valid express
					if not self.is_key_word(t):
						self.write_error(t['line'], 'Invalid str \'{}\'.'.format(t['value']))
					while not self.is_end() and not self.is_key_word(t):
						t = self.get_next_token()
					self.return_before_token()
					break
			else:
				self.write_error(t['line'], 'Invalid str \'{}\'.'.format(t['value']))
				while not self.is_end() and not self.is_key_word(t):
						t = self.get_next_token()

		print dealed_list
		self.print_info('Express analysis done.')
		a = self.token[start_index:self.now_token_index]
		return self.gene_middle_code(a)
		# return self.token[start_index:self.now_token_index]

	def deal_bracket(self):
		t = self.get_next_token()
		while t['value'] != ')' and not self.is_key_word(t):
			if t['value'] == '(':
				self.deal_bracket()
			else:
				self.return_before_token()
				self.deal_express(True)
			t = self.get_next_token()
		pass

	def deal_math_expr(self, expr):
		s = []
		for e in expr:
			if e['value'] in ('+', '-', '*', '/', '<=', '>=', '==', '<>', '<', '>'):
				e2 = s.pop()
				e1 = s.pop()
				self.print_middle_code(e['value'], e1['value'], e2['value'], 't{}'.format(self.t_index))
				s.append({'value':'t{}'.format(self.t_index)})
				self.t_index += 1
			else:
				s.append(e)
		return s.pop()['value']

	def deal_if(self):
		if self.is_end():
			return
		self.print_info('Analysing IF sentence...')
		self.out_index += 4
		expr = self.deal_express()
		to_fill_else_index = []
		to_fill_then_index = []
		for ie in expr['e']:
			e = self.deal_math_expr(ie)
			if len(expr['c']) == 0:
				# if a then...
				self.print_middle_code('jnz', e, '_', '')
				to_fill_then_index.append(self.get_mid_length()-1)
				self.print_middle_code('j', '_', '_', '')
				to_fill_else_index.append(self.get_mid_length()-1)
			else:
				# There are rops
				r = expr['c'].pop()
				if r['value'] == 'or':
					self.print_middle_code('jnz', e, '_', '')
					to_fill_then_index.append(self.get_mid_length()-1)
					self.print_middle_code('j', '_', '_', self.get_mid_length() + 2)
				elif r['value'] == 'and':
					self.print_middle_code('jnz', e, '_', self.get_mid_length() + 3)
					self.print_middle_code('j', '_', '_', '')
					to_fill_else_index.append(self.get_mid_length()-1)
		t = self.get_next_token()
		if t['value'] == 'then':
			for item in to_fill_then_index:
				self.result['mid'][item][3] = self.get_mid_length() + 1
			self.deal_instruct()
			t = self.get_next_token()
			t = self.get_next_token()
			for item in to_fill_else_index:
				self.result['mid'][item][3] = self.get_mid_length() + 1
			if t is not None and t['value'] == 'else':
				self.deal_instruct()
			else:
				self.return_before_token()
		else:
			self.write_error(t['line'], 'Missing \'then\' at line {}.'.format(t['line']))
		self.out_index -= 4
		self.print_info('If setence analysis done.')
		# self.return_before_token()

	def deal_for(self):
		self.print_info('Analysing FOR sentence...')
		self.out_index += 4
		v = self.deal_instruct(True)
		t = self.get_next_token()
		to_fill_end = 0
		if t['value'] != 'to':
			self.print_info('Missing \'to\' in for sentence.')
		else:
			e = self.deal_math_expr(self.deal_express()['e'][0])
			self.print_middle_code('j>', v, e, '')
			to_fill_end = self.get_mid_length() - 1
			# self.print_middle_code('j', '_', '_', '')
			t = self.get_next_token()
			if t['value'] != 'do':
				self.print_info('Missing \'do\' in for sentence.')
			else:
				t = self.get_next_token()
				if t['value'] == 'begin':
					self.deal_begin()
				else:
					self.return_before_token()
					self.deal_instruct()
		self.print_middle_code('j', '_', '_', to_fill_end + 1)
		self.result['mid'][to_fill_end][3] = self.get_mid_length() + 1
		self.out_index -= 4
		self.print_info('For setence analysis done.')

	def deal_while(self):
		self.print_info('Analysing WHILE setence...')
		self.out_index += 4
		self.deal_express()
		# t = self.get_next_token()
		# if t['value'] != 'do':
		# 	self.write_error(t['line'], 'Missing \'do\' in WHILE setence.')
		# 	# self.read_to_instruct_end()
		# 	return
		t = self.get_next_token()
		if t['value'] == 'begin':
			self.deal_begin()
		else:
			while not self.is_key_word(t):
				self.deal_instruct()
		self.out_index -= 4
		self.print_info('While setence analysis done.')

	def deal_repeat(self):
		# t = self.get_next_token()
		self.print_info('Analysing REPEAT setence...')
		self.out_index += 4
		self.deal_instruct()
		t = self.get_next_token()
		if t['value'] != 'until':
			self.write_error(t['line'], 'Missing \'until\' in REPEAT setence.')
		else:
			self.deal_instruct()
		self.out_index -= 4
		self.print_info('Repeat setence analysis done.')

	def deal_instruct(self, is_need_end = False):
		if self.is_end():
			return
		t = self.get_next_token()
		try:
			self.module_func[t['value']]()
			self.return_before_token()
			return
		except Exception:
			pass
		self.print_info('Analysing instruct...')
		self.out_index += 4
		if not self.is_var(t):
			self.write_error(t['line'], 'Invalid instruct start with \'{}\''.format(t['value']))
			#self.read_to_instruct_end()
			return
		if self.is_valid_var(t['value']) and self.is_valid_const(t['value']):
			self.write_error(t['line'], 'Undefined var \'{}\''.format(t['value']))
		v = t
		t = self.get_next_token()
		if t['value'] == ':':
			t = self.get_next_token()
			if t['value'] != '=':
				self.write_error(t['line'], 'Missing \'=\' before \'{}\''.format(t['value']))
				#self.read_to_instruct_end()
				return
			else:
				# such as a := 1;
				t = self.get_next_token()
				if not self.is_const(t):
					# is not const
					self.write_error(t['line'], '\'{}\' is not a const.'.format(t['value']))
					#self.read_to_instruct_end()
					return
				self.print_middle_code('=', t['value'], '_', v['value'])
		elif t['value'] == '=':
			# such as a = 1+23/23;
			expr = self.deal_express()
			e = ''
			for ie in expr['e']:
				e = self.deal_math_expr(ie)
			t = self.get_next_token()
			if t['value'] != ';':
				t = self.return_before_token()
				if not is_need_end:
					self.write_error(t['line'], 'Unexcept end of instruct at \'{}\''.format(t['value']))
					self.return_before_token()
			self.print_middle_code('=', e, '_', v['value'])

		self.out_index -= 4
		self.print_info('Instruct setence analysis done.')
		return v['value']

	def read_to_instruct_end(self):
		t = self.get_next_token()
		while t['value'] != ';' and not self.is_key_word(t):
			t = self.get_next_token()
		self.return_before_token()

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
		return t['key'] <= 17

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
		return 35 <= t['key'] <= 38 or 18 <= t['key'] <= 20

	def is_user_set_const(self, t):
		return

	def is_var_type(self, t):
		return 3<=t['key'] <=6

	def is_middle_symbol(self, t):
		return 22<=t['key'] <=33

	def write_error(self, line, err):
		self.result['error'] += 'Line {}: {}\n'.format(line, err)
		print err

	def is_valid_const(self, c):
		x = not [x for x in self.const_table if x['name'] == c]
		return x

	def is_valid_var(self, c):
		x = not [x for x in self.var_table if x['name'] == c]
		return x

	def is_middle_symbol(self, t):
		return 22<=t['key'] <=33

	def print_middle_code(self, j, v1, v2, t):
		self.result['mid'].append([j, v1, v2, t])

	def get_mid_length(self):
		return len(self.result['mid'])