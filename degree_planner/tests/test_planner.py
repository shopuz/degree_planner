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


	def test_available_units_in_session(self):
		dp = Degree_Planner('BIT', 'SOT01', '2011', 's1')
		
		available_units = dp.get_available_units()
		self.assertEqual(available_units, ['COMP115'])

		student_units = ['COMP115']
		available_units = dp.get_available_units(student_units)
		self.assertNotEqual(available_units, ['COMP125', 'DMTH137', 'ISYS114'])

		dp = Degree_Planner('BIT', 'SOT01', '2011', 's2')
		available_units = dp.get_available_units(student_units)
		self.assertEqual(available_units, ['COMP125', 'DMTH137', 'ISYS114'])

	def test_available_units_in_entire_degree(self):
		dp = Degree_Planner('BIT', 'SOT01', '2011', 's1')
		
		available_units = dp.get_available_units_for_entire_degree()
		expected_result = {'2011': [{'s1': ['COMP115']}, {'s2': ['COMP125', 'DMTH137', 'ISYS114']}], '2013': [{'s1': ['COMP355']}, {'s2': []}], '2012': [{'s1': ['DMTH237']}, {'s2': ['COMP255', 'ISYS224']}]}
		self.assertEqual(available_units, expected_result)

	def test_update_general_requirements(self):
		pp = Prereq_Parser()
		handbook = Handbook()
		student_units = ['COMP115', 'COMP125', 'DMTH137', 'ISYS114',  'DMTH237', 'COMP255', 'ISYS224', 'COMP355']
		gen_degree_req = handbook.extract_general_requirements_of_degree('BIT', '2014')
		result = pp.update_general_requirements_of_degree(student_units, gen_degree_req)
		expected_result = {             'min_total_cp': 48,
										'min_200_above': 30,
										'min_300_above': 15,
										'min_designation_information_technology': 18,
										'foundation_units': 0
									}

		self.assertEqual(result, expected_result)

	def test_all_units_prior_to_session(self):
		dp = Degree_Planner('BIT', 'SOT01', '2011', 's1')
		student_units_json = {'2011': [{'s1': ['COMP115']}, {'s2': ['COMP125', 'DMTH137', 'ISYS114']}], '2012': [{'s1': ['DMTH237']}, {'s2': ['COMP255', 'ISYS224']}], '2013': [{'s1': ['COMP355']}, {'s2': []}]}
		
		all_units_prior_to_session = dp.get_all_units_prior_to_session(student_units_json, '2012', 's1')
		expected_result = ['COMP115', 'COMP125', 'DMTH137', 'ISYS114']
		self.assertEqual(sorted(all_units_prior_to_session), sorted(expected_result))

		all_units_prior_to_session = dp.get_all_units_prior_to_session(student_units_json, '2012', 's2')
		expected_result = ['COMP115', 'COMP125', 'DMTH137', 'ISYS114', 'DMTH237']
		self.assertEqual(sorted(all_units_prior_to_session), sorted(expected_result))

		all_units_prior_to_session = dp.get_all_units_prior_to_session(student_units_json, '2011', 's1')
		expected_result = []
		self.assertEqual(sorted(all_units_prior_to_session), sorted(expected_result))

		all_units_prior_to_session = dp.get_all_units_prior_to_session(student_units_json, '2011', 's2')
		expected_result = ['COMP115']
		self.assertEqual(sorted(all_units_prior_to_session), sorted(expected_result))

		all_units_prior_to_session = dp.get_all_units_prior_to_session(student_units_json, '2013', 's2')
		expected_result = ['COMP115', 'COMP125', 'DMTH137', 'ISYS114', 'DMTH237', 'COMP255', 'ISYS224', 'COMP355']
		self.assertEqual(sorted(all_units_prior_to_session), sorted(expected_result))
	
	
	
	
	 # filter_units_by_prereq
