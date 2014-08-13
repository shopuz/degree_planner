from pyparsing import *
import re

class Prereq_Parser():
	def __init__(self):
		self.atomic = Word(alphanums)
		self.obr = oneOf('[(')
		self.cbr = oneOf(')]')
		self.complex = (self.atomic + self.obr + self.cbr)
		self.complex_expr = OneOrMore(self.complex)
		self.simple_expr = operatorPrecedence(self.atomic, [
									("and", 2, opAssoc.LEFT, self.expandChainedExpr),
									("or", 2, opAssoc.LEFT, self.expandChainedExpr ),
								])

		self.complex_keywords = ['from', 'including', '-']
		#self.parsed_list = None
		
	def parse_string(self, prereq=None):
		""" Pyparsing module to tokenize the prerequisite with 'and' and 'or' logical operators
			Parses the structure into a binary tree representation
		"""
		if  self.prereq_check(prereq):

			result =  self.simple_expr.parseString(prereq).asList()
			#result = self.arrange_operator(result[0])
			return result[0]
			
		else:
			split_list = re.split(" including | from ", prereq)

			result = ParseResults([])
			result  += ParseResults(self.parse_string(split_list[0]))
			result += ParseResults(['including'])

			split_list = split_list[1:]
			
			for item in split_list:
				result += ParseResults([self.parse_string(item)])
				#result = self.complex_expr.parseString(prereq).asList()
			return list(result)

	def prereq_check(self, prereq):
		for word in self.complex_keywords:
			if word in prereq:
				return False
		return True

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

	# Not used for now but might require later
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
	def __init__(self):
		self.cp_rule = {"undergraduate": 3, "postgraduate": 4}
		word = Word(alphas)
		num = Word(nums)
 		self.ncp = num + word
		


	# Calculate the total credit points obtained by the student based on his completed units
	def total_cp(self, student_units, level="undergraduate"):
		total_cp_gained = len(student_units) * self.cp_rule[level]
		return total_cp_gained

	def evaluate_prerequisite(self, pre_req_tree, student_units ):
		""" 
			['COMP125', 'or', 'COMP165'] 
			['COMP225', 'or', 'COMP229', 'or', 'COMP125']
		"""
		if isinstance(pre_req_tree, str):
			if pre_req_tree in student_units:
				return True
			else:
				if 'cp' in pre_req_tree:
					cp = int(self.ncp.parseString(pre_req_tree)[0])
					if cp == self.total_cp(student_units):
						return True

				return False
		elif isinstance(pre_req_tree, list):
			# do recursive call
			if pre_req_tree[1] == 'or':
				temp = str(self.evaluate_prerequisite(pre_req_tree[0], student_units) or self.evaluate_prerequisite(pre_req_tree[2], student_units))
				return eval(temp)
			elif pre_req_tree[1] == 'and' or pre_req_tree[1] == 'including':
				temp = str(self.evaluate_prerequisite(pre_req_tree[0], student_units) and self.evaluate_prerequisite(pre_req_tree[2], student_units))
				print temp
				return eval(temp)


if __name__ == '__main__':
	pp = Prereq_Parser()
	pre_req = '18cp including (COMP115 or COMP155)'
	#pre_req = 'COMP125 or COMP165'
	#pre_req = 'COMP225 or COMP229 or COMP125'

	print pp.parse_string(pre_req)
