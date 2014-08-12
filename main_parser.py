from pyparsing import *
import unittest


class Prereq_Parser():
	def __init__(self):
		self.atomic = Word(alphanums)
		self.expr = operatorPrecedence(self.atomic, [
									("AND", 2, opAssoc.LEFT, ),
									("OR", 2, opAssoc.LEFT, ),
								])
		self.parsed_list = None
		
	def parse_string(self, prereq=None):
		""" Pyparsing module to tokenize the prerequisite with AND and OR logical operators
			Parses the structure into a binary tree representation
		"""
		result =  self.expr.parseString(prereq, parseAll=True).asList()
		result = self.arrange_operator(result[0])
		return result

	def arrange_operator(self, parsed_list):
		"""
		Input: 	Parsed List from pyparsing
			 	[['COMP115', 'OR', 'COMP125'], 'AND', 'MATH132']
		
		Output: Binary Tree representation of form [operator, unit, unit]
				['AND', ['OR', 'COMP115', 'COMP125'], 'MATH132']

		"""
		if len(parsed_list) == 3:
			first_var = parsed_list[0]
			parsed_list[0] = parsed_list[1]
			parsed_list[1] = first_var

			for value in parsed_list:
				if isinstance(value, list):
					self.arrange_operator(value)

		return parsed_list


	def evaluate_prerequisite(self, pre_req_tree, student_units ):
		""" ['OR', 'COMP115', 'COMP125'] """
		if isinstance(pre_req_tree, str):
			if pre_req_tree in student_units:
				return True
			else:
				return False
		elif isinstance(pre_req_tree, list):
			# do recursive call
			if pre_req_tree[0] == 'OR':
				temp = str(self.evaluate_prerequisite(pre_req_tree[1], student_units) or self.evaluate_prerequisite(pre_req_tree[2], student_units))
				print temp
				return eval(temp)
			elif pre_req_tree[0] == 'AND':
				temp = str(self.evaluate_prerequisite(pre_req_tree[1], student_units) and self.evaluate_prerequisite(pre_req_tree[2], student_units))
				print temp
				return eval(temp)
		

		

class ParseTestCase(unittest.TestCase):
	""" Various Tests related to Parsing a Prerequisite 	"""

	def test_simple_logical(self):
		pp = Prereq_Parser()
		
		result = pp.parse_string("COMP115 AND COMP125")
		expected_result = ['AND', 'COMP115', 'COMP125']
		self.assertEqual(result, expected_result)
		
		result = pp.parse_string("(COMP115 OR COMP125) AND MATH132")
		expected_result = ['AND', ['OR', 'COMP115', 'COMP125'], 'MATH132']
		self.assertEqual(result, expected_result)

		result = pp.parse_string("(COMP165 AND ((COMP115 OR COMP125) OR (MATH132 OR MATH136)))")
		expected_result = ['AND', 'COMP165', ['OR', ['OR', 'COMP115', 'COMP125'], ['OR', 'MATH132', 'MATH136' ]]]
		self.assertEqual(result, expected_result)

	def test_evaluate_prereq(self):
		pp = Prereq_Parser()
		pre_req_tree = ['OR', 'COMP115', 'COMP125']
		student_units = ['COMP125', 'COMP115', 'COMP165']
		self.assertTrue(pp.evaluate_prerequisite(pre_req_tree, student_units))

		pre_req_tree = ['AND', ['OR', 'COMP115', 'COMP125'], 'MATH132']
		self.assertFalse(pp.evaluate_prerequisite(pre_req_tree, student_units))

		student_units = ['COMP115', 'MATH132']
		pre_req_tree = ['AND', ['OR', 'COMP115', 'COMP125'], 'MATH132']
		self.assertTrue(pp.evaluate_prerequisite(pre_req_tree, student_units))		

if __name__ == "__main__":
	unittest.main(verbosity=2)
	