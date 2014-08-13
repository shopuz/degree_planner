import unittest
from degree_planner.prereq_parser import *

class ParseTestCase(unittest.TestCase):
	""" Various Tests related to Parsing a Prerequisite 	"""

	def test_simple_logical(self):
		pp = Prereq_Parser()
		
		result = pp.parse_string('COMP115')
		expected_result = 'COMP115'
		self.assertEqual(result, expected_result)
		result = pp.parse_string('COMP125 or COMP165')
		expected_result = ['COMP125','or', 'COMP165']
		self.assertEqual(result, expected_result)

		result = pp.parse_string('COMP225 or COMP229 or COMP125')
		expected_result = [['COMP225', 'or', 'COMP229'], 'or', 'COMP125']
		self.assertEqual(result, expected_result)

		result = pp.parse_string('COMP115 and (COMP111 or INFO111 or MAS111)')
		expected_result = ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']]
		self.assertEqual(result, expected_result)

	def test_evaluate_prereq(self):
		pp = Prereq_Parser()
		ev = Evaluate_Prerequisite()
		pre_req_tree = ['COMP115', 'or', 'COMP125']
		student_units = ['COMP125', 'COMP115', 'COMP165']
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		pre_req_tree = [['COMP225', 'or', 'COMP229'], 'or', 'COMP125']
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		student_units =['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']]
		self.assertFalse(ev.evaluate_prerequisite(pre_req_tree, student_units))		

if __name__ == '__main__':
	unittest.main(verbosity=2)
