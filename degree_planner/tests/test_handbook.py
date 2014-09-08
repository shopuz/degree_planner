import unittest
from degree_planner.degree_parser import *
from degree_planner.handbook import *


class HandbookTestCase(unittest.TestCase):
	
	def test_extract_unit_designation(self):
		handbook = Handbook()
		unit_designations = handbook.extract_unit_designation('COMP115', '2014')
		expected_designations = ['Engineering', 'Information Technology', 'Science', 'Technology']
		self.assertEqual(unit_designations, expected_designations)

		unit_designations = handbook.extract_unit_designation('BBA102', '2014')
		expected_designations = ['Commerce', 'Engineering']
		self.assertEqual(unit_designations, expected_designations)


	def test_extract_all_majors_of_degree(self):
		handbook = Handbook()
		all_majors = handbook.extract_all_majors_of_degree('BIT', '2013')
		expected_majors = {	'SOT01': 'Software Technology', 
							'BUI01': 'Business Information Systems'
						  }
		self.assertEqual(all_majors, expected_majors)

		all_majors = handbook.extract_all_majors_of_degree('BCom', '2014')
		expected_majors = { 'ACC02': 'Accounting',
							'BUI01': 'Business Information Systems',
							'DES01' :'Decision Science',
							'ECO02' : 'Economics',
							'FIN01' : 'Finance',
							'HUR02' : 'Human Resources',
							'INB02' : 'International Business',
							'MAR02' : 'Marketing'
						}
		self.assertEqual(all_majors, expected_majors)

	def test_extract_general_requirements_of_degree(self):
		handbook = Handbook()
		gen_reqs = handbook.extract_general_requirements_of_degree('BIT', '2014')
		expected_gen_reqs = {	'min_total_cp': 72,
								'min_200_above': 42,
								'min_300_above': 18,
								'min_designation_information_technology': 42,
								'foundation_units': 12
							}
		self.assertEqual(gen_reqs, expected_gen_reqs)

		gen_reqs = handbook.extract_general_requirements_of_degree('BCom', '2014')
		expected_gen_reqs = {	'min_total_cp' : 69,
								'min_200_above' : 39,
								'min_300_above' : 18,
								'min_designation_commerce' : 42,
								'foundation_units' : 15
							}
		self.assertEqual(gen_reqs, expected_gen_reqs)


	def test_extract_degree_requirements(self):
		handbook = Handbook()
		deg_req_units = handbook.extract_degree_requirements('BIT', '2014')
		expected_deg_req_units = ['COMP115', 'DMTH137', 'ISYS114', 'ISYS224']
		self.assertEqual(deg_req_units, expected_deg_req_units)

		deg_req_units = handbook.extract_degree_requirements('BCom', '2014')
		expected_deg_req_units = ['ACST101', 'BBA102', 'ECON111', 'MKTG101', 'ACCG100 or ACCG106' ]
		self.assertEqual(deg_req_units, expected_deg_req_units)


	def test_extract_major_requirements(self):
		handbook = Handbook()
		major_reqs = handbook.extract_major_requirements('SOT01', '2014')
		expected_major_reqs = ['COMP115', 'COMP125', 'DMTH137', 'COMP255', 'DMTH237', 'COMP225 or COMP229', '3cp from COMP units at 200 level', 'COMP355', '9cp from COMP300-COMP350 or ISYS326']
		self.assertEqual(sorted(major_reqs), sorted(expected_major_reqs))

		major_reqs = handbook.extract_major_requirements('ECO02', '2014')
		expected_major_reqs =['ECON110', 'ECON111', 'STAT170 or STAT171', 'ECON203', 'ECON204', 'ECON241', 'ECON309', 'ECON350', '6cp from ECON303 or ECON311 or ECON334 or ECON335 or ECON336 or ECON356 or ECON359 or ECON360 or ECON361 or ECON394',]
		self.assertEqual(sorted(major_reqs), sorted(expected_major_reqs))


	# update_degree_req_units
	# update_major_reqs
	# filter_units_by_offering
	
