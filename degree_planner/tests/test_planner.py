import unittest
from degree_planner.degree_parser import *
from degree_planner.handbook import *
from degree_planner.degree_planner import *

class DegreePlannerTestCase(unittest.TestCase):
	def test_get_all_units_prior_to_session(self):
		dp = Degree_Planner('BIT', 'SOT01', '2013', 's1')
		student_units_json = {'2011': [{'s1': ['COMP115']}, {'s2': ['COMP125', 'DMTH137', 'ISYS114']}], '2013': [{'s1': ['COMP355']}, {'s2': []}], '2012': [{'s1': ['DMTH237']}, {'s2': ['COMP255', 'ISYS224']}]}
		[year, session] = ['2012', 's2']
		units_prior_2012_s2 = dp.get_all_units_prior_to_session(student_units_json, year, session)
		expected_result = ['COMP115', 'COMP125', 'DMTH137', 'ISYS114', 'DMTH237']

		self.assertEqual(units_prior_2012_s2, expected_result)