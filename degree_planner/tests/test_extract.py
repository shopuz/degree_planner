import unittest
from degree_planner.parser import *
from degree_planner.handbook import *


class ExtractTestCase(unittest.TestCase):
	def test_extract_unit_designation(self):
		handbook = Handbook()
		unit_designations = handbook.extract_unit_designation('COMP115', '2014')
		expected_designations = ['Engineering', 'Information Technology', 'Science', 'Technology']
		self.assertEqual(unit_designations, expected_designations)