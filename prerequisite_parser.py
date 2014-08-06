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
alphanum_brackets = pp.Word(pp.alphanums + "(" + ")" )
nw_cp = num + "cp" 
range_expr = wn + "-" + wn
# 3cp from MATH132-MATH136
pre_req_syntax_1 = nw_cp + ( word + range_expr )

# 18cp including (COMP115 or COMP155)
pre_req_syntax_2 = nw_cp + "including" + alphanum_brackets

# prereq unit range MATH132-MATH136 = ['MATH132', 'MATH133', 'MATH134', 'MATH135', 'MATH136']
unit_range = []
cp_rule = {"undergraduate": 3, "postgraduate": 4}
syntax1_flag = False
syntax2_flag = False

student_units = [ 'COMP115', 'COMP165', 'MATH132', 'DMTH137', 'MATH134', 'MATH135', 'MATH136']
#student_units = ['COMP125', 'MATH136']
#main_pre_req = pre_req =  "(COMP125(P) or COMP165(P)) and (3cp(P) from MATH132-MATH136 or DMTH137)"
main_pre_req = pre_req = "18cp including (COMP115 or COMP155)"

# Calculate Total Credit Points obtained by the student
# To check "3cp from MATH132-MATH136"
# unit_list = [ 'MATH132', 'MATH133', 'MATH134', 'MATH135', 'MATH136' ]
def cp_calculator(student_units, unit_list):
	cp = 0
	for student_unit in student_units:
		if student_unit in unit_list:
			cp = cp + 3
	return cp

# Calculate the total credit points obtained by the student based on his completed units
def total_cp(student_units, level="undergraduate"):
	total_cp_gained = len(student_units) * cp_rule[level]
	return total_cp_gained


def prepare_unit_range(unit_name, starting_unit, ending_unit):
	i = starting_unit
	while i <= ending_unit:
		unit_range.append(unit_name + str(i))
		i = i + 1


def parse_pre_req_syntax_1(text):
	global pre_req
	# tokens = (['3', 'cp', 'from', 'MATH', '132', '-', 'MATH', '136'], {})
	if syntax1_flag:
		tokens = list(pre_req_syntax_1.parseString(text))
		# if the prerequisite contains a range
	
		range_index = tokens.index('-')
		unit_name = tokens[range_index + 1]
		starting_unit = int(tokens[range_index - 1])
		ending_unit = int(tokens[range_index + 2])
		prepare_unit_range(unit_name, starting_unit, ending_unit)
		cp_required = int(tokens[0])

		if cp_calculator(student_units, unit_range) == cp_required:
			complex_statement_result = "True"
			pre_req = pre_req.replace(complex_statement, complex_statement_result)
		else:
			pre_req = pre_req.replace(complex_statement, "False")
	
	elif syntax2_flag:
		tokens = list(pre_req_syntax_2.parseString(text))
		total_cp_gained = total_cp(student_units)
		cp_required = int(tokens[0])
		pre_req = pre_req.replace("including", "and")

		if total_cp_gained >= cp_required:
			pre_req = pre_req.replace(str(cp_required) + "cp", "True")
		else:
			pre_req = pre_req.replace(str(cp_required) + "cp", "False")


if __name__ == '__main__':
	

	negative_words = [ 'or', 'and', 'including', 'from']

	
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
				syntax1_flag = True

		for t,s,e in pre_req_syntax_2.scanString(req):
			if t:
				# for structure 18cp including COMP115
				# need to convert 18cp into True or False as well
				complex_statements.append(req)
				syntax2_flag = True

	#print "complex statements: ", complex_statements
	for complex_statement in complex_statements:
		parse_pre_req_syntax_1(complex_statement)

	pre_req_unit_list = re.split(' and | or | including ', cleaned_pre_req)
	# filtered_list = ['COMP125', 'COMP165', 'MATH132-MATH136', 'DMTH137']
	filtered_list = [ x for x in pre_req_unit_list if ((x not in negative_words) and ('cp' not in x)) ]
	#print 'pre_req_unit_list: ', pre_req_unit_list
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
	print "student_units: ", student_units
	print "main prerequisite statement: ", main_pre_req
	print "pre_req: " , pre_req
	print "------------------------"
	if (eval(pre_req) == True):
		print 'Result: Yes'
	else:
		print 'Result: No'

	print "------------------------"


# Replace 3cp from MATH132-MATH136 with true or false in the statement