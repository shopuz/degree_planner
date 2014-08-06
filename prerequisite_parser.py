"""
	Author: Suren
 	Sample Prerequisite for COMP225 : "(COMP125(P) or COMP165(P)) and (3cp(P) from MATH132-MATH136 or DMTH137)"
 	Input: COMP125, DMTH137
 	Output : Yes

 """

import re
import pyparsing as pp


""" 
Some Grammars:
3cp from MATH132-MATH136 = num_word + word + range


"""

word = pp.Word(pp.alphas)
num = pp.Word(pp.nums)
wn = word + num
nw = num + word 
range_expr = wn + "-" + wn
pre_req_syntax_1 = nw + ( word + range_expr )


# prereq unit range MATH132-MATH136 = ['MATH132', 'MATH133', 'MATH134', 'MATH135', 'MATH136']
unit_range = []

# Calculate Total Credit Points obtained by the student
# To check "3cp from MATH132-MATH136"
# unit_list = [ 'MATH132', 'MATH133', 'MATH134', 'MATH135', 'MATH136' ]
def cp_calculator(student_units, unit_list):
	cp = 0
	for student_unit in student_units:
		if student_unit in unit_list:
			cp = cp + 3
	return cp


def prepare_unit_range(unit_name, starting_unit, ending_unit):
	i = starting_unit
	while i <= ending_unit:
		unit_range.append(unit_name + str(i))
		i = i + 1


def parse_pre_req_syntax_1(text):
	# tokens = (['3', 'cp', 'from', 'MATH', '132', '-', 'MATH', '136'], {})
	tokens = list(pre_req_syntax_1.parseString(text))
	cp_required = int(tokens[0])

	unit_name = tokens[tokens.index('-') + 1]
	starting_unit = int(tokens[tokens.index('-') - 1])
	ending_unit = int(tokens[tokens.index('-') + 2])
	prepare_unit_range(unit_name, starting_unit, ending_unit)
	return cp_required



if __name__ == '__main__':
	student_units = [ 'DMTH137', 'COMP165']

	negative_words = [ 'or', 'and', 'including', 'from']

	pre_req =  "(COMP125(P) or COMP165(P)) and (3cp(P) from MATH132-MATH136 or DMTH137)"
	pre_req = pre_req.replace('(P)', '')

	# pre_req = "(COMP125 or COMP165) and (3cp from MATH132-MATH136 or DMTH137)"
	cleaned_pre_req = pre_req.replace('(', '').replace(')', '')
	pre_req_unit_list = re.split(' and | or ', cleaned_pre_req)
	# complex_statements = ['3cp from MATH132-MATH136']
	complex_statements = []
	for req in pre_req_unit_list:
		for t,s,e in pre_req_syntax_1.scanString(req):
			if t:
				complex_statements.append(req)


	for complex_statement in complex_statements:
		cp_required = parse_pre_req_syntax_1(complex_statement)
		if cp_calculator(student_units, unit_range) == cp_required:
			complex_statement_result = "True"
			pre_req = pre_req.replace(complex_statement, complex_statement_result)
		else:
			pre_req = pre_req.replace(complex_statement, "False")


	# filtered_list = ['COMP125', 'COMP165', 'MATH132-MATH136', 'DMTH137']
	filtered_list = [ x for x in pre_req_unit_list if x not in negative_words ]
	#print 'filtered list: ', filtered_list

	# Set all the units taken by student to True
	for unit in student_units:
		globals()[unit] = True

	# If there are any units whose value is not set above, set them to False
	for unit in filtered_list:
		if unit not in globals():
			globals()[unit] = False



	#unit_list = [ 'MATH132', 'MATH133', 'MATH134', 'MATH135', 'MATH136' ]
	#complex_statement = "3cp from MATH132-MATH136"

	#print "pre_req: " , pre_req
	if (eval(pre_req) == True):
		print 'Yes'
	else:
		print 'No'



# Replace 3cp from MATH132-MATH136 with true or false in the statement