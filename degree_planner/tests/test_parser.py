import unittest
from degree_planner.prereq_parser import *

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
		self.assertTrue(pp.evaluate_prerequisite(pre_req_tree, student_units))		

if __name__ == "__main__":
	unittest.main(verbosity=2)
