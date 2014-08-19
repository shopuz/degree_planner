import re
from pyparsing import *
from compiler.ast import flatten
import time
import urllib, json
from extract import *

class Prereq_Parser():
	def __init__(self):
		self.word = Word(alphas)
		self.nums = Word(nums)
		self.wn = self.word + self.nums

		self.atomic = Word(alphanums)
		self.obr = oneOf('[(')
		self.cbr = oneOf(')]')
		self.complex = (self.atomic + self.obr + self.cbr)
		self.complex_expr = OneOrMore(self.complex)
		self.simple_expr = operatorPrecedence(self.atomic, [
									("and", 2, opAssoc.LEFT, self.expandChainedExpr),
									("or", 2, opAssoc.LEFT, self.expandChainedExpr ),
								])

		self.complex_keywords = ['from', 'including', '-', 'units']
		#self.parsed_list = None

	def parse_unit_range(self, unit_range):
		"""
		Return the list of units from within a given unit_range
		Input: MATH132-MATH136
		Output: "MATH132 or MATH133 or MATH134 or MATH135 or MATH136"

		"""
		unit_range_list = unit_range.split("-")
		[unit_code, initial_unit_number] = self.wn.parseString(unit_range_list[0]).asList()
		[unit_code, final_unit_number] = self.wn.parseString(unit_range_list[1]).asList()

		result_string = unit_range_list[0] + " "
		i = int(initial_unit_number) + 1
		while i <= int(final_unit_number):
			result_string += "or " + unit_code + str(i) + " "
			i = i + 1


		return result_string[:-1]

	
	def parse_unit_levels(self, prereq=None):
		"""
		Parse the structure like : "3cp from COMP or ISYS units at 100 level"
		Get the units of that level from Handbook API

		Input: "3cp from COMP or ISYS units at 100 level"
		Todo:
		Output: "3cp from COMP111 or COMP115 or COMP125 or COMP188 or ISYS104 or ISYS114"

		"""
		[cp, units, level] = filter(None, re.split(" from | units at | level", prereq))
		level = int(level)

		prereq_units = re.split(" and | or ", units)
		handbook = Handbook()
		# Todo: check undergraduate / postgraduate from level and pass into the following function
		all_units_at_level =  handbook.extract_all_units_of_level(2014, level, "undergraduate")

		filtered_unit_list = [unit for unit in all_units_at_level if self.wn.parseString(unit)[0] in prereq_units]
		
		new_prereq_string = filtered_unit_list[0] + " "
 		for unit in filtered_unit_list[1:]:
			new_prereq_string += 'or ' + unit + ' '
		new_prereq_string = new_prereq_string[:-1]
		string_to_be_replaced = prereq.split(" from ")[1]
		new_prereq = prereq.replace(string_to_be_replaced, new_prereq_string)
		
		return new_prereq







	def parse_string(self, prereq=None):
		""" Pyparsing module to tokenize the prerequisite with 'and' and 'or' logical operators
			Parses the structure into a binary tree representation
		"""
		from_flag = False
		if  self.prereq_check(prereq):
			
			result =  self.simple_expr.parseString(prereq).asList()
			#result = self.arrange_operator(result[0])
			return result[0]
			
		else:
			if '-' in prereq:
				keyword = None
				split_list = prereq.split(" ")

				unit_range = [word for word in split_list if '-' in word][0]
				# remove brackets [()] from unit_range
				unit_range = re.sub(r"[\[()\]]", "", unit_range)

				parsed_unit_range = self.parse_unit_range(unit_range)
				prereq = prereq.replace(unit_range, parsed_unit_range)
				
				return self.parse_string(prereq)

			elif 'including' in prereq:
				keyword = 'including'
				split_list = re.split(' ' + keyword + ' ', prereq)
			elif 'units' in prereq:
				return self.parse_string(self.parse_unit_levels(prereq))

			elif 'from' in prereq:
				keyword = 'from'
				temp_pre_req_list = prereq.split(" ")
				from_index = temp_pre_req_list.index("from")
				
				if from_index > 1:
					split_keyword = temp_pre_req_list[from_index -2]
					
					split_list = prereq.split(split_keyword + " ")
					split_list[0] = split_list[0] + split_keyword
					
					keyword = split_keyword
					

					split_list = [x.replace("(", "").replace(")", "") for x in split_list ]

					result = ParseResults([])
					result  += ParseResults([self.parse_string(split_list[0])])
					from_flag = True

				else:
					split_list = re.split(' ' + keyword + ' ', prereq)
			
				#split_list = ['(COMP125 or COMP165)', 'and', '(3cp from MATH132-MATH136 or DMTH137)']
			
			#time.sleep(5)
			
			if not from_flag:
				result = ParseResults([])
				result  += ParseResults(self.parse_string(split_list[0]))
			
			if keyword:
				result += ParseResults([keyword]) 

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

	def evaluate_from(self, pre_req_tree, student_units):
		"""
			Evaluate statements containing 'from'
			Eg: 9cp from (ACCG355 or ACCG358 or ISYS301 or ISYS302 or ISYS360 or MPCE360)
		"""
		# TOdo : find the level (undergrad/postgrad) from student_units
		level = "undergraduate"
		# Flatten the deeply nested list into a single top level list
		# [[[[['ACCG355', 'or', 'ACCG358'], 'or', 'ISYS301'], 'or', 'ISYS302'], 'or', 'ISYS360'], 'or', 'MPCE360'] 
		# into ['ACCG355', 'or', 'ACCG358', 'or', 'ISYS301', 'or', 'ISYS302', 'or', 'ISYS360', 'or', 'MPCE360']
		pre_req_units = flatten(pre_req_tree)
		# Get the common units from student units and prereq_units so that 
		# total cp from prereq_units can be calculated
		common_units = list(set(pre_req_units).intersection(set(student_units)))
		total_cp_gained = len(common_units) * self.cp_rule[level]

		# Find the required cp from pre_req_tree
		for item in pre_req_tree:
		    if 'cp' in item:
		        required_cp = int(self.ncp.parseString(item)[0])

		if total_cp_gained >= required_cp:
			return True
		else:
			return False


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
					if self.total_cp(student_units) >= cp:
						return True

				return False
		elif isinstance(pre_req_tree, list):
			
			if 'from' in pre_req_tree:
				return self.evaluate_from(pre_req_tree, student_units)

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
	#pre_req = '18cp including (COMP115 or COMP155)'
	#pre_req = 'COMP125 or COMP165'
	#pre_req = 'COMP225 or COMP229 or COMP125'
	#pre_req = '(COMP125 or COMP165 and (3cp from MATH132-MATH136 or DMTH137))'
	#pre_req = '3cp from (MATH132-MATH136 or DMTH137)'
	#pre_req = '(COMP125 or COMP165) and (3cp from MATH132-MATH136 or DMTH137)'
	#[['COMP125', 'or', 'COMP165'], 'and', ['3cp', 'from', [[[[['MATH132', 'or', 'MATH133'], 'or', 'MATH134'], 'or', 'MATH135'], 'or', 'MATH136'], 'or', 'DMTH137']]]
	pre_req = '3cp from COMP or ISYS units at 100 level'
	print 'result: '
	print pp.parse_string(pre_req)
	
	
