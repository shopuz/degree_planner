from prereq_parser import *
from handbook import *
from datetime import date

class Degree_Planner():

	def __init__(self, degree_code=None, major_code=None):
		self.degree_code = degree_code
		self.major_code = major_code
		


	def available_units(self, student_units=None, session="S2"):
		# 1. Get all units from Major Requirements
		# 2. Filter the list with current unit offerings
		# 3. Get prereq of each unit
		# 4. Parse and Evaluate each prereq
		# 5. Finally prepare the list of all units which passed the prereq evaluation
		
		handbook = Handbook()
		parser = Prereq_Parser()
		ev = Evaluate_Prerequisite()
		
		#print session
		final_available_units = []

		# Todo: Remove this and make it more robust.
		# Can be done only after the parser can handle situations like admission / permission etc.
		temp_complex_units = {
								'COMP125' : 'COMP115(P) or COMP155(P)', 
								'COMP188' :	'', 
								'COMP365' : '39cp and COMP225(P) and (COMP227(P) or COMP255(P) or ISYS227(P))',
								'COMP388' :	'39cp and COMP188'
							}

		major_units = handbook.extract_major_req_units('SOT01', '2014')
		print 'major_units: ', major_units

		# filtered_unit_list : list of units available in the session
		filtered_unit_list = []
		print 'student_units: ', student_units

		for unit in major_units:
			unit_offerings = handbook.extract_unit_offering_of_unit(unit, '2014')
			# unit_offerings : ['s1 day', 's1 evening', 's3 day']
			# unit_offerings_session_codes : ['s1', 's1', 's3']
			# Just to know whether the unit is offered in the session or not

			unit_offerings_session_codes = [ unit_offering.split(" ")[0] for unit_offering in unit_offerings]
			print unit_offerings_session_codes
			if session.lower() in unit_offerings_session_codes and unit not in student_units:
				filtered_unit_list.append(unit)

		print 'filtered_unit_list: ', filtered_unit_list
		print '------------------------------'
		for unit in filtered_unit_list:
			if unit in temp_complex_units.keys():
				pre_req = temp_complex_units[unit]
			else:
				pre_req = handbook.extract_pre_req_for_unit(unit, '2014')

			# Todo: Parse the grade  (P, Cr) as well
			pre_req = pre_req.replace("(P)", "").replace("(Cr)", "")
			#print unit, ' : ' , pre_req
			
			
			if not pre_req and unit not in final_available_units:
				#print 'no pre_req so continuing'
				final_available_units.append(unit)
				continue
			
			#print 'trying to parse prereq'
			pre_req_tree = parser.parse_string(pre_req)
			print unit , ' : ' , pre_req_tree

			evaluate_result = ev.evaluate_prerequisite(pre_req_tree, student_units)
			print 'evaluate_result: ', evaluate_result
			print '-----------------------------'
			if evaluate_result and unit not in final_available_units:
				final_available_units.append(unit)

		return final_available_units



if __name__ == '__main__':
	dp = Degree_Planner('BIT', 'SOT01')
	student_units = ['COMP115']
	session = "S2"
	#student_units = ['COMP125', 'COMP115', 'COMP165', 'MAS111', 'INFO111', 'DMTH237']
	print 'Available Units'
	print dp.available_units(student_units, session)
