from pyparsing import *

class Prereq_Parser():
	def __init__(self):
		self.atomic = Word(alphanums)
		self.expr = operatorPrecedence(self.atomic, [
									("and", 2, opAssoc.LEFT, self.expandChainedExpr),
									("or", 2, opAssoc.LEFT, self.expandChainedExpr ),
								])
		self.parsed_list = None
		
	def parse_string(self, prereq=None):
		""" Pyparsing module to tokenize the prerequisite with 'and' and 'or' logical operators
			Parses the structure into a binary tree representation
		"""
		result =  self.expr.parseString(prereq).asList()
		#result = self.arrange_operator(result[0])
		return result[0]

	def expandChainedExpr(self, tokens):
		"""
			Function to order the sequence of operands and operators based on their precedence.
			Initial Prerequisite = 'COMP115 and (COMP111 or INFO111 or MAS111)'
			Input: tokens = ['COMP115', 'and', 'COMP111', 'or', 'INFO111', 'or', 'MAS111']
			Output: ret = ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']]
		"""
		tokeniter = iter(tokens[0])
		firstexpr = next(tokeniter)
		# zips = [('or', 'COMP125'), ('and', 'MATH132')]
		zips = zip(tokeniter,tokeniter)

		ret = ParseResults([firstexpr])
		zip_length = len(zips)
		# ret = [['COMP124', 'or', 'COMP125']]
		ret = ret + ParseResults(list(zips[0]))	
		
		# Loop through the zips if there are more than 1 items in zips
		i = 1
		while i < zip_length:
			ret = ParseResults([ret]) + ParseResults(list(zips[i]))
			i = i + 1
		
		return [ret]

	def arrange_operator(self, parsed_list):
		"""
		Input: 	Parsed List from pyparsing
				[['COMP115', 'or', 'COMP125'], 'and', 'MATH132']
		
		Output: Binary Tree representation of form [operator, unit, unit]
				['and', ['or', 'COMP115', 'COMP125'], 'MATH132']

		"""
		if len(parsed_list) == 3:
			first_var = parsed_list[0]
			parsed_list[0] = parsed_list[1]
			parsed_list[1] = first_var

			for value in parsed_list:
				if isinstance(value, list):
					self.arrange_operator(value)

		return parsed_list


class Evaluate_Prerequisite():
	def evaluate_prerequisite(self, pre_req_tree, student_units ):
		""" 
			['COMP125', 'or', 'COMP165'] 
			['COMP225', 'or', 'COMP229', 'or', 'COMP125']
		"""
		if isinstance(pre_req_tree, str):
			if pre_req_tree in student_units:
				return True
			else:
				return False
		elif isinstance(pre_req_tree, list):
			# do recursive call
			if pre_req_tree[1] == 'or':
				temp = str(self.evaluate_prerequisite(pre_req_tree[0], student_units) or self.evaluate_prerequisite(pre_req_tree[2], student_units))
				return eval(temp)
			elif pre_req_tree[1] == 'and':
				temp = str(self.evaluate_prerequisite(pre_req_tree[0], student_units) and self.evaluate_prerequisite(pre_req_tree[2], student_units))
				print temp
				return eval(temp)
