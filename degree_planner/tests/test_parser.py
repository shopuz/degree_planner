import unittest
from degree_planner.degree_parser import *
from degree_planner.degree_planner import *
from degree_planner.handbook import *

class ParseTestCase(unittest.TestCase):
    """ Various Tests related to Parsing a Prerequisite     """

    def test_simple_logical(self):
        pp = Prereq_Parser()
        test_samples = {
            'COMP115'                                                   : 'COMP115',
            'COMP125 or COMP165'                                        : ['COMP125','or', 'COMP165'],
            'COMP225 or COMP229 or COMP125'                             : [['COMP225', 'or', 'COMP229'], 'or', 'COMP125'],
            'COMP115 and (COMP111 or INFO111 or MAS111)'                : ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']],
            '(COMP125 or COMP165) and (DMTH137 or MATH237 or DMTH237)'  : [['COMP125', 'or', 'COMP165'], 'and', [['DMTH137', 'or', 'MATH237'], 'or', 'DMTH237']],
            'COMP247 and COMP125 and (MATH237 or DMTH237 or DMTH137 or ELEC240)' : [['COMP247', 'and', 'COMP125'],'and', [[['MATH237', 'or', 'DMTH237'], 'or', 'DMTH137'], 'or', 'ELEC240']],
            # Some advanced structures
            '18cp including (COMP115 or COMP155)'                       : ['18cp', 'including', ['COMP115', 'or', 'COMP155']],
            '39cp including ((COMP225 or COMP229) and (COMP255 or COMP227 or ISYS227))': ['39cp', 'including', [['COMP225', 'or', 'COMP229'], 'and', [['COMP255', 'or', 'COMP227'], 'or', 'ISYS227']]],

            # keyword : from
            '9cp from (ACCG355 or ACCG358 or ISYS301 or ISYS302 or ISYS360 or MPCE360)' : ['9cp', 'from', [[[[['ACCG355', 'or', 'ACCG358'], 'or', 'ISYS301'], 'or', 'ISYS302'], 'or', 'ISYS360'], 'or', 'MPCE360']],
            '3cp from MATH132-MATH136 or DMTH137'   : ['3cp', 'from', [[[[['MATH132', 'or', 'MATH133'], 'or', 'MATH134'], 'or', 'MATH135'], 'or', 'MATH136'], 'or', 'DMTH137']],
            '3cp from (MATH132-MATH136 or DMTH137)' : ['3cp', 'from', [[[[['MATH132', 'or', 'MATH133'], 'or', 'MATH134'], 'or', 'MATH135'], 'or', 'MATH136'], 'or', 'DMTH137']],
            '(COMP125 or COMP165) and (3cp from MATH132-MATH136 or DMTH137)'    :   [['COMP125', 'or', 'COMP165'], 'and', ['3cp', 'from', [[[[['MATH132', 'or', 'MATH133'], 'or', 'MATH134'], 'or', 'MATH135'], 'or', 'MATH136'], 'or', 'DMTH137']]],

            # advanced keyword : from
            '3cp from COMP or ISYS units at 100 level'  :   ['3cp', 'from', [[[[['COMP111', 'or', 'COMP115'], 'or', 'COMP125'], 'or', 'COMP188'], 'or', 'ISYS104'], 'or', 'ISYS114']]
            }

        for pre_req in test_samples.keys():
            result = pp.parse_string(pre_req)
            self.assertEqual(result, test_samples[pre_req])

        

    def test_evaluate_prereq(self):
        pp = Prereq_Parser()
        ev = Evaluate_Prerequisite()
        # First Student units
        student_units = {'COMP125' : 'P', 'COMP115' : 'P', 'COMP165' : 'P', 'MAS111' : 'P'}

        pre_req_tree = ['COMP115', 'or', 'COMP125']
        graded_pre_req = {'COMP111': 'P', 'INFO111': 'P', 'MAS111': 'P', 'COMP115': 'P', 'COMP125': 'P', 'COMP165': 'P', 
                            'COMP225' : 'P', 'COMP227': 'P', 'COMP229': 'P', 'COMP247': 'P', 'MATH237': 'P', 'DMTH137': 'P', 'DMTH237': 'P', 'ELEC240' : 'P',
                            'ISYS100': 'P', 'ISYS104': 'P', 'ISYS114': 'P', 'ISYS224': 'P', 'ISYS254': 'P', 'ISYS301': 'P', 'MPCE360': 'P', 'ACCG355': 'P',
                            '9cp': 'P'}
        self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))

        pre_req_tree = [['COMP225', 'or', 'COMP229'], 'or', 'COMP125']
        self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))

        
        pre_req_tree = ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']]
        self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))

        # Second Student units
        student_units = {'COMP125' : 'P', 'COMP115' : 'P', 'COMP165' : 'P'}
        pre_req_tree = ['COMP115', 'and', [['COMP111' , 'or', 'INFO111'], 'or', 'MAS111']]
        self.assertFalse(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))

        # Third Student units
        pre_req_tree = [['COMP247', 'and', 'COMP125'],'and', [[['MATH237', 'or', 'DMTH237'], 'or', 'DMTH137'], 'or', 'ELEC240']]
        self.assertFalse(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))
        student_units = {'COMP247': 'P', 'COMP125': 'P', 'DMTH137': 'P'}
        self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))

        # Fourth Student Units
        student_units = {'COMP125': 'P', 'COMP115': 'P', 'COMP165': 'P', 'MAS111': 'P', 'INFO111': 'P', 'DMTH237': 'P'}
        pre_req_tree = ['18cp', 'including', ['COMP115', 'or', 'COMP155']]
        self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))

        # Fifth Student Units
        student_units = {'COMP125': 'P', 'COMP115': 'P', 'COMP165': 'P', 'MAS111': 'P', 'INFO111': 'P', 'DMTH237': 'P', 'COMP225': 'P', 'COMP227': 'P', 'ISYS100': 'P', 'ISYS104': 'P', 'ISYS114': 'P', 'ISYS224': 'P', 'ISYS254': 'P', 'ISYS301': 'P', 'MPCE360': 'P'}
        pre_req_tree = ['39cp', 'including', [['COMP225', 'or', 'COMP229'], 'and', [['COMP255', 'or', 'COMP227'], 'or', 'ISYS227']]]
        self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))

        pre_req_tree = ['9cp', 'from', [[[[['ACCG355', 'or', 'ACCG358'], 'or', 'ISYS301'], 'or', 'ISYS302'], 'or', 'ISYS360'], 'or', 'MPCE360']]
        self.assertFalse(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))
        
        # Sixth Student units
        student_units = {'COMP125': 'P', 'COMP115': 'P', 'COMP165': 'P', 'MAS111': 'P', 'INFO111': 'P', 'DMTH237': 'P', 'COMP225': 'P', 'ACCG355': 'P', 'ISYS100': 'P', 'ISYS104': 'P', 'ISYS114': 'P', 'ISYS224': 'P', 'ISYS254': 'P', 'ISYS301': 'P', 'MPCE360': 'P'}
        self.assertTrue(ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req))


    def test_process_students(self):
        pp = Prereq_Parser('BIT', '2014')
        print 'testing process students'
        student_units = ['COMP115', 'COMP125', 'DMTH137', 'ISYS114',  'DMTH237', 'COMP255', 'ISYS224', 'COMP355']
        result = pp.process_student_units(student_units)
        expected_result = {
                            "TOTAL_CP": 24,
                            "designation_commerce": 3,
                            "designation_engineering": 15,
                            "designation_information_technology": 24,
                            "designation_science": 24,
                            "designation_technology": 18,
                            "foundation_units": 12,
                            "level": {
                                "100": {
                                    "COMP": 6,
                                    "DMTH": 3,
                                    "ISYS": 3,
                                    "TOTAL_CP": 12
                                },
                                "200": {
                                    "COMP": 3,
                                    "DMTH": 3,
                                    "ISYS": 3,
                                    "TOTAL_CP": 9
                                },
                                "300": {
                                    "COMP": 3,
                                    "TOTAL_CP": 3
                                }
                            }
                        }
        self.assertEqual(result,expected_result)

    


#if __name__ == '__main__':
#   unittest.main(verbosity=2)
