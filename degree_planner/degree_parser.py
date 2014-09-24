import re
import time
import urllib, json

from handbook import *
from pyparsing import *
from compiler.ast import flatten

class Prereq_Parser():
    def __init__(self, degree_code='', year=''):
        self.word = Word(alphas)
        self.nums = Word(nums)
        self.wn = self.word + self.nums
        # unit with grade COMP125(P)
        self.wn_grade = self.wn + '(' + oneOf('P Cr S') + ')'

        self.atomic = Word(alphanums)
        self.obr = oneOf('[ (')
        self.cbr = oneOf(') ]')
        self.complex = (self.atomic + self.obr + self.cbr)

        self.complex_expr = OneOrMore(self.complex)

        self.simple_expr = operatorPrecedence(self.atomic, [
                                    ("and", 2, opAssoc.LEFT, self.expandChainedExpr),
                                    ("or", 2, opAssoc.LEFT, self.expandChainedExpr ),
                                ])

        self.complex_keywords = ['from', 'including', '-', 'units']
        self.degree_code = degree_code
        self.year = year
        self.grades = ['P', 'Cr']
        self.graded_pre_req = {}
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
        # Store the graded pre requisite
        self.store_graded_pre_req(prereq)

        from_flag = False
        prereq = prereq.replace('(P)', '').replace('(Cr)', '').replace('[', '(').replace(']', ')').replace(' in ', ' from ').strip()

        if  self.prereq_check(prereq):
            #print 'pre_req in parser: ', prereq
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
            #print 'split_list: ', split_list
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
        """
            Check if the prereq is complex (i.e 'from', 'including', '-', 'units at 100 level' etc)
            Return : True (prereq is simple)
                     False (prereq is complex)
        """
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
        Input:  Parsed List from pyparsing
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

    def get_stored_cp(self, parsed_student_units, level, unit_code):
        """ Return the cp stored in parsed_student_units """
        if unit_code in parsed_student_units['level'][level]:
            cp = parsed_student_units['level'][level][unit_code]
        else:
            cp = 0
        
        return cp


    def store_graded_pre_req(self, pre_req):
        """ Store the graded pre_req """
        
        pre_req = pre_req.split(' ')
        for grade in self.grades:
            for req in pre_req:
                if '(' + grade + ')' in req:
                    req = req.replace('(' + grade + ')', '').replace('(', '').replace(')', '')
                    self.graded_pre_req[req]= grade
                else:
                    req = req.replace('(', '').replace(')', '')
                    self.graded_pre_req[req]= 'None'


        


  

    def process_student_units(self, student_units=[]):
        """
        Get detailed information about student units.
        Input :['COMP115', 'COMP125', 'DMTH137', 'ISYS114',  'DMTH237', 'COMP255', 'ISYS224', 'COMP355']
        Output: {
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
        """

        handbook = Handbook()

        parsed_student_units ={ 'level': {'100':{}, '200':{}, '300':{}} }
        total_cp_100 = total_cp_200 = total_cp_300 = foundation_units_total_cp = 0
        unit_designations = []
        foundation_units = handbook.get_foundation_units(self.degree_code, self.year)
        
        ev = Evaluate_Prerequisite()
        
        print 'in process_student_units ', student_units
        print 'foundation units: ', foundation_units

        for unit in student_units:
            [ unit_code, unit_number ] = self.wn.parseString(unit)
            if unit_number.startswith('1'):
                parsed_student_units['level']['100'][unit_code] = self.get_stored_cp(parsed_student_units, '100', unit_code) + 3
                total_cp_100 += 3
            elif unit_number.startswith('2'):
                parsed_student_units['level']['200'][unit_code] = self.get_stored_cp(parsed_student_units, '200', unit_code) + 3
                total_cp_200 += 3
            elif unit_number.startswith('3'):
                parsed_student_units['level']['300'][unit_code] = self.get_stored_cp(parsed_student_units, '300', unit_code) + 3
                total_cp_300 += 3

            

            # ['Engineering', 'Information Technology', 'Science', 'Technology']
            unit_designations += handbook.extract_unit_designation(unit, self.year)

        # Evaluate Foundation Units
        for foundation_unit in foundation_units:
            pre_req_tree = self.parse_string(foundation_unit)

            evaluate_result = ev.evaluate_prerequisite(pre_req_tree, student_units, self.graded_pre_req)

            if evaluate_result:
                foundation_units_total_cp += 3
                

        parsed_student_units['level']['100']['TOTAL_CP'] = total_cp_100
        parsed_student_units['level']['200']['TOTAL_CP'] = total_cp_200
        parsed_student_units['level']['300']['TOTAL_CP'] = total_cp_300

        parsed_student_units['foundation_units'] = foundation_units_total_cp

        for designation in list(set(unit_designations)):
            parsed_student_units['designation_' + designation.lower().replace(' ', '_')] = unit_designations.count(designation) * 3

        parsed_student_units['TOTAL_CP'] = parsed_student_units['level']['100']['TOTAL_CP'] + parsed_student_units['level']['200']['TOTAL_CP'] + parsed_student_units['level']['300']['TOTAL_CP']

        #print parsed_student_units
        return parsed_student_units

    def update_general_requirements_of_degree(self, student_units, gen_reqs):
        """
        Based on parsed student units, update the general requirements of the degree
        Input : gen_reqs : {    'min_total_cp': 72,
                                'min_200_above': 42,
                                'min_300_above': 18,
                                'min_designation_information_technology': 42,
                                'foundation_units': 12
                            }
                parsed_student_units : {
                                        'level': { 
                                                    '100': {
                                                            'COMP' : 6,
                                                            'DMTH' : 3,
                                                            'ISYS' : 3,
                                                            'TOTAL_CP': 12
                     
                                                    },
                                                    '200': {
                                                            'COMP' : 3,
                                                            'DMTH' : 3,
                                                            'ISYS' : 3,
                                                            'TOTAL_CP': 9
                     
                                                    },
                                                    '300': {
                                                            'COMP' : 3,
                                                            'TOTAL_CP': 3
                     
                                                    }

                                        },
                                        'foundation' : 12,
                                        'TOTAL_CP' : 24,
                                        'designation_information_technology': 24

                                    }
        Output:  modified_gen_reqs : {  'min_total_cp': 48,
                                        'min_200_above': 30,
                                        'min_300_above': 15,
                                        'min_designation_information_technology': 18,
                                        'foundation_units': 0
                                    }

        """
        handbook = Handbook()
        parsed_student_units = self.process_student_units(student_units)
        #gen_reqs = handbook.extract_general_requirements_of_degree(degree_code, year)
        
        print 'parsed_student_units: ', parsed_student_units

        modified_gen_reqs = gen_reqs.copy()
        keys = gen_reqs.keys()
        for key in gen_reqs.keys():
            if key == 'min_total_cp':
                updated_value = modified_gen_reqs['min_total_cp'] - parsed_student_units['TOTAL_CP']
                modified_gen_reqs['min_total_cp'] = 0 if (updated_value < 0) else updated_value
            elif key == 'min_200_above':
                min_200_above_from_student_units = parsed_student_units['level']['200']['TOTAL_CP'] + parsed_student_units['level']['300']['TOTAL_CP']
                updated_value =modified_gen_reqs['min_200_above'] - min_200_above_from_student_units
                modified_gen_reqs['min_200_above'] = 0 if (updated_value < 0) else updated_value
            elif key == 'min_300_above':
                min_300_above_from_student_units = parsed_student_units['level']['300']['TOTAL_CP']
                updated_value = modified_gen_reqs['min_300_above'] - min_300_above_from_student_units
                modified_gen_reqs['min_300_above'] = 0 if (updated_value < 0) else updated_value
            elif key == 'foundation_units':
                updated_value = modified_gen_reqs['foundation_units'] - parsed_student_units['foundation_units']
                modified_gen_reqs['foundation_units'] = 0 if (updated_value < 0) else updated_value
            elif key == 'min_designation_information_technology':
                updated_value =  modified_gen_reqs['min_designation_information_technology'] - parsed_student_units['designation_information_technology']       
                modified_gen_reqs['min_designation_information_technology'] = 0 if (updated_value < 0) else updated_value
            elif 'designation' in key:
                updated_key = key.split('min_')[1].lower()
                updated_value = modified_gen_reqs[key] - parsed_student_units[updated_key]
                modified_gen_reqs[key] = 0 if (updated_value<0) else updated_value

        
        return modified_gen_reqs


    def update_degree_req_units(self, student_units, degree_req_units):
        """
        Update the degree requirement units by verifying the requirement with student units
        """
        remaining_units = list(set(degree_req_units) - set(student_units))
        return remaining_units

    def update_major_reqs(self, student_units, major_reqs):
        """
        Update the major requirement units by verifying the requirement with student units
        """
        print 'updating major requirements'
        print 'student_units: ', student_units
        print 'major_reqs: ', major_reqs
        
        remaining_reqs = list(set(major_reqs) - set(student_units))
        #complex_req_units = [req for req in major_reqs if " " in req]
        final_remaining_reqs = []
        evaluator = Evaluate_Prerequisite()
        
        for req in remaining_reqs:
            pre_req_tree = self.parse_string(req)

            result = evaluator.evaluate_prerequisite(pre_req_tree, student_units)
            if not result:
                final_remaining_reqs.append(req)

        return final_remaining_reqs

    def update_degree_major_reqs(self, student_units, degree_major_reqs):
        """
        Update the major requirement units by verifying the requirement with student units
        """
        
        remaining_reqs = list(set(degree_major_reqs) - set(student_units))
        #complex_req_units = [req for req in degree_major_reqs if " " in req]
        satisfied_reqs = []
        evaluator = Evaluate_Prerequisite()
        print student_units
        for req in remaining_reqs:
            pre_req_tree = self.parse_string(req)

            result = evaluator.evaluate_prerequisite(pre_req_tree, student_units)
            if result:
                satisfied_reqs.append(req)

        return list(set(remaining_reqs) - set(satisfied_reqs))







class Evaluate_Prerequisite():
    def __init__(self):
        self.cp_rule = {"undergraduate": 3, "postgraduate": 4}
        word = Word(alphas)
        num = Word(nums)
        self.ncp = num + word
        self.grade_values = {   'None' : -1,
                                'F' : 0,
                                'P' : 1,
                                'Cr': 2,
                                'D' : 3,
                                'HD': 4
                                }
        


    # Calculate the total credit points obtained by the student based on his completed units
    #@staticmethod
    def total_cp(self, student_units, level="undergraduate", graded_pre_req={}):
        total_cp_gained = 0
        print 'student units in total_cp : ', student_units.keys()
        for unit in student_units.keys():
            total_cp_gained = total_cp_gained + self.cp_rule[level]
            
        return total_cp_gained

    def find_required_cp(self, pre_req_tree):
        # Find the required cp from pre_req_tree
        for item in pre_req_tree:
            if 'cp' in item:
                required_cp = int(self.ncp.parseString(item)[0])
                return required_cp

    def evaluate_from(self, pre_req_tree, student_units, graded_pre_req={}):
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
        common_units = list(set(pre_req_units).intersection(set(student_units.keys())))
        
        common_student_units = {}

        for unit in common_units:
            common_student_units[unit] = student_units[unit]
        
        print 'student units: ', student_units
        print 'common_student_units: ', common_student_units

        common_student_units_grade = self.grade_values.keys()[self.grade_values.values().index(max([self.grade_values[grade] for grade in common_student_units.values()]))]

        print 'common_student_units_grade: ', common_student_units_grade
        total_cp_gained = self.total_cp(common_student_units, level, graded_pre_req)

        # Find the required cp from pre_req_tree
        for item in pre_req_tree:
            if 'cp' in item:
                required_cp = int(self.ncp.parseString(item)[0])

        print 'total_cp_gained: ', total_cp_gained
        print 'required_cp: ', required_cp
        print 'graded_pre_req: ', graded_pre_req
        print "self.grade_values[graded_pre_req[str(required_cp)+'cp']]", self.grade_values[graded_pre_req[str(required_cp)+'cp']]
        print "self.grade_values[common_student_units_grade] : ", self.grade_values[common_student_units_grade]
        if total_cp_gained >= required_cp and self.grade_values[graded_pre_req[str(required_cp)+'cp']] <= self.grade_values[common_student_units_grade]:
            return True
        else:
            return False


    def evaluate_prerequisite(self, pre_req_tree, student_units , graded_pre_req={}):
        """ 
            ['COMP125', 'or', 'COMP165'] 
            ['COMP225', 'or', 'COMP229', 'or', 'COMP125']
        """
        print 'pre_req_tree : ',  pre_req_tree

        if isinstance(student_units, list):
            temp_student_units = student_units
            student_units = {}
            for unit in temp_student_units:
                student_units[unit] = 'None'

            print 'student_units: ', student_units

        print 'graded_pre_req: ', graded_pre_req
        if isinstance(pre_req_tree, str):
            
            if pre_req_tree in student_units.keys() and self.grade_values[student_units[pre_req_tree]] >= self.grade_values[graded_pre_req[pre_req_tree]] :
                return True
            elif pre_req_tree == 'True':
                return True
            elif pre_req_tree == 'False':
                return False
            else:
                if 'cp' in pre_req_tree:
                    cp = int(self.ncp.parseString(pre_req_tree)[0])
                    if self.total_cp(student_units) >= cp:
                        return True

                return False
        elif isinstance(pre_req_tree, list):
            
            if 'from' in pre_req_tree:
                return self.evaluate_from(pre_req_tree, student_units, graded_pre_req)

            # do recursive call
            if pre_req_tree[1] == 'or':
                temp = str(self.evaluate_prerequisite(pre_req_tree[0], student_units, graded_pre_req) or self.evaluate_prerequisite(pre_req_tree[2], student_units, graded_pre_req))
                return eval(temp)
            elif pre_req_tree[1] == 'and' or pre_req_tree[1] == 'including':
                temp = str(self.evaluate_prerequisite(pre_req_tree[0], student_units, graded_pre_req) and self.evaluate_prerequisite(pre_req_tree[2], student_units, graded_pre_req))
                #print temp
                return eval(temp)

    


if __name__ == '__main__':
    pp = Prereq_Parser()
    #pre_req = '18cp including (COMP115 or COMP155)'
    #pre_req = 'COMP125 or COMP165'
    #pre_req = 'COMP225 or COMP229 or COMP125'
    #pre_req = '(COMP125 or COMP165 and (3cp from MATH132-MATH136 or DMTH137))'
    #pre_req = '3cp from (MATH132-MATH136 or DMTH137)'
    pre_req = '(COMP125(P) or COMP165(P)) and (3cp(P) from MATH132-MATH136 or DMTH137)'
    # [['COMP125', 'or', 'COMP165'], 'and', ['3cp', 'from', [[[[['MATH132', 'or', 'MATH133'], 'or', 'MATH134'], 'or', 'MATH135'], 'or', 'MATH136'], 'or', 'DMTH137']]]
    #pre_req = '3cp from COMP or ISYS units at 100 level'
    #pre_req = '39cp and COMP125 or COMP249'
    #pre_req = ''
    #print 'result: '
    print pp.parse_string(pre_req)
    pre_req_tree = pp.parse_string(pre_req)
    graded_pre_req = pp.graded_pre_req
    print 'graded_pre_req: ', graded_pre_req
    student_units = {'COMP125' : 'P', 'DMTH137' : 'D'}
    ev = Evaluate_Prerequisite()
    print ev.evaluate_prerequisite(pre_req_tree, student_units, graded_pre_req)
    #pre_req = '6cp from COMP or ISYS or ACCG or STAT or BUS or BBA units at 200 level'
    #print pre_req
    
    """
    student_units = ['COMP115', 'COMP125', 'DMTH137', 'ISYS114',  'DMTH237', 'COMP255', 'ISYS224', 'COMP355']
    #print json.dumps(pp.process_student_units(student_units), indent=4, sort_keys=True)
    handbook = Handbook()
    gen_req = handbook.extract_general_requirements_of_degree('BIT', '2014')
    print 'result'
    print '===================='
    print pp.update_general_requirements_of_degree(student_units, gen_req)
    """
    
