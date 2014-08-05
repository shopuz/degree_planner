"""
	Author: Suren
 	Sample Prerequisite : "(COMP125(P) or COMP165(P)) and (3cp(P) from MATH132-MATH136 or DMTH137)"
 	Input: COMP125, DMTH137
 	Output : Yes

 """

# Calculate Total Credit Points obtained by the student
# To check "3cp from MATH132-MATH136"
# unit_list = [ 'MATH132', 'MATH133', 'MATH134', 'MATH135', 'MATH136' ]
def cp_calculator(student_units, unit_list):
	cp = 0
	for student_unit in student_units:
		if student_unit in unit_list:
			cp = cp + 3
	return cp



if __name__ == '__main__':
	pre_req =  "(COMP125(P) or COMP165(P)) and (3cp(P) from MATH132-MATH136 or DMTH137)"
	negative_words = [ 'or', 'and', 'including', 'from']
	student_units = ['COMP165', 'COMP125', 'MATH137']

	pre_req = "(COMP125 or COMP165) and (3cp from MATH132-MATH136 or DMTH137)"
	cleaned_pre_req = pre_req.replace('(P)', '').replace('(', '').replace(')', '')
	pre_req_unit_list = cleaned_pre_req.split(" ")
	# filtered_list = ['COMP125', 'COMP165', 'MATH132-MATH136', 'DMTH137']
	filtered_list = [ x for x in pre_req_unit_list if x not in negative_words ]
	print 'filtered list: ', filtered_list

	# Set all the units taken by student to True
	for unit in student_units:
		globals()[unit] = True

	# If there are any units whose value is not set above, set them to False
	for unit in filtered_list:
		if unit not in globals():
			globals()[unit] = False



	unit_list = [ 'MATH132', 'MATH133', 'MATH134', 'MATH135', 'MATH136' ]
	complex_statement = "3cp from MATH132-MATH136"

	if cp_calculator(student_units, unit_list) == 3:
		complex_statement_result = "True"
		pre_req = pre_req.replace(complex_statement, complex_statement_result)
	else:
		pre_req = pre_req.replace(complex_statement, "False")


	if (eval(pre_req) == True):
		print 'Yes'
	else:
		print 'No'



# Replace 3cp from MATH132-MATH136 with true or false in the statement