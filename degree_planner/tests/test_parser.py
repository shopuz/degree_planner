import unittest
from degree_planner.prereq_parser import *

class ParseTestCase(unittest.TestCase):
	""" Various Tests related to Parsing a Prerequisite 	"""

	def test_simple_logical(self):
		pp = Prereq_Parser()
		test_samples = {
			'COMP115' 													: 'COMP115',
			'COMP125 or COMP165' 										: ['COMP125','or', 'COMP165'],
			'COMP225 or COMP229 or COMP125'								: [['COMP225', 'or', 'COMP229'], 'or', 'COMP125'],
			'COMP115 and (COMP111 or INFO111 or MAS111)' 				: ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']],
			'(COMP125 or COMP165) and (DMTH137 or MATH237 or DMTH237)' 	: [['COMP125', 'or', 'COMP165'], 'and', [['DMTH137', 'or', 'MATH237'], 'or', 'DMTH237']],
			'COMP247 and COMP125 and (MATH237 or DMTH237 or DMTH137 or ELEC240)' : [['COMP247', 'and', 'COMP125'],'and', [[['MATH237', 'or', 'DMTH237'], 'or', 'DMTH137'], 'or', 'ELEC240']],
			# Some advanced structures
			'18cp including (COMP115 or COMP155)'						: ['18cp', 'including', ['COMP115', 'or', 'COMP155']],
			'39cp including ((COMP225 or COMP229) and (COMP255 or COMP227 or ISYS227))': ['39cp', 'including', [['COMP225', 'or', 'COMP229'], 'and', [['COMP255', 'or', 'COMP227'], 'or', 'ISYS227']]],

			# keyword : from
			'9cp from (ACCG355 or ACCG358 or ISYS301 or ISYS302 or ISYS360 or MPCE360)' : ['9cp', 'from', [[[[['ACCG355', 'or', 'ACCG358'], 'or', 'ISYS301'], 'or', 'ISYS302'], 'or', 'ISYS360'], 'or', 'MPCE360']],
			'3cp from MATH132-MATH136 or DMTH137'	: ['3cp', 'from', [[[[['MATH132', 'or', 'MATH133'], 'or', 'MATH134'], 'or', 'MATH135'], 'or', 'MATH136'], 'or', 'DMTH137']],
			'3cp from (MATH132-MATH136 or DMTH137)'	: ['3cp', 'from', [[[[['MATH132', 'or', 'MATH133'], 'or', 'MATH134'], 'or', 'MATH135'], 'or', 'MATH136'], 'or', 'DMTH137']]
			}

		for pre_req in test_samples.keys():
			result = pp.parse_string(pre_req)
			self.assertEqual(result, test_samples[pre_req])

		

	def test_evaluate_prereq(self):
		pp = Prereq_Parser()
		ev = Evaluate_Prerequisite()
		# First Student units
		student_units = ['COMP125', 'COMP115', 'COMP165', 'MAS111']

		pre_req_tree = ['COMP115', 'or', 'COMP125']
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		pre_req_tree = [['COMP225', 'or', 'COMP229'], 'or', 'COMP125']
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		
		pre_req_tree = ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']]
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		# Second Student units
		student_units = ['COMP125', 'COMP115', 'COMP165']
		pre_req_tree = ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']]
		self.assertFalse(ev.evaluate_prerequisite(pre_req_tree, student_units))

		# Third Student units
		pre_req_tree = [['COMP247', 'and', 'COMP125'],'and', [[['MATH237', 'or', 'DMTH237'], 'or', 'DMTH137'], 'or', 'ELEC240']]
		self.assertFalse(ev.evaluate_prerequisite(pre_req_tree, student_units))
		student_units = ['COMP247', 'COMP125', 'DMTH137']
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		# Fourth Student Units
		student_units = ['COMP125', 'COMP115', 'COMP165', 'MAS111', 'INFO111', 'DMTH237']
		pre_req_tree = ['18cp', 'including', ['COMP115', 'or', 'COMP155']]
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		# Fifth Student Units
		student_units = ['COMP125', 'COMP115', 'COMP165', 'MAS111', 'INFO111', 'DMTH237', 'COMP225', 'COMP227', 'ISYS100', 'ISYS104', 'ISYS114', 'ISYS224', 'ISYS254', 'ISYS301', 'MPCE360']
		pre_req_tree = ['39cp', 'including', [['COMP225', 'or', 'COMP229'], 'and', [['COMP255', 'or', 'COMP227'], 'or', 'ISYS227']]]
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))

		pre_req_tree = ['9cp', 'from', [[[[['ACCG355', 'or', 'ACCG358'], 'or', 'ISYS301'], 'or', 'ISYS302'], 'or', 'ISYS360'], 'or', 'MPCE360']]
		self.assertFalse(ev.evaluate_prerequisite(pre_req_tree, student_units))

		# Sixth Student units
		student_units = ['COMP125', 'COMP115', 'COMP165', 'MAS111', 'INFO111', 'DMTH237', 'COMP225', 'ACCG355', 'ISYS100', 'ISYS104', 'ISYS114', 'ISYS224', 'ISYS254', 'ISYS301', 'MPCE360']
		self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units))
#if __name__ == '__main__':
#	unittest.main(verbosity=2)
