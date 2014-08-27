from prereq_parser import *
from handbook import *
from datetime import date
import math
import itertools

class Degree_Planner():

	def __init__(self, degree_code=None, major_code=None):
		self.degree_code = degree_code
		self.major_code = major_code
		


	def get_available_units(self, year, session, student_units=[], 
								all_core_units=None, remaining_requirements=None):
		"""
		Get the available units in the given year and session.
		Output: ['COMP115']
		"""
		handbook = Handbook()
		parser = Prereq_Parser()
		ev = Evaluate_Prerequisite()
		
		final_available_units = []

		# Todo: Remove this and make it more robust.
		# Can be done only after the parser can handle situations like admission / permission etc.
		temp_complex_units = {
								'COMP125' : 'COMP115(P) or COMP155(P)', 
								'COMP188' :	'', 
								'COMP247' :	'3cp from COMP or ISYS units at 100 level',
								'COMP365' : '39cp and COMP225(P) and (COMP227(P) or COMP255(P) or ISYS227(P))',
								'COMP388' :	'39cp and COMP188'
							}
		if not all_core_units:
			degree_requirements = handbook.extract_degree_requirements(self.degree_code, year)
			major_requirements = handbook.extract_major_req_units(self.major_code, year)

			major_units = [ unit for unit in major_requirements if len(unit.split(" ")) == 1 ]
			degree_units = [ unit for unit in degree_requirements if len(unit.split(" ")) == 1 ]
			remaining_requirements = list(set(degree_requirements).union(set(major_requirements)) - set(major_units).union(set(degree_units)) )
			all_core_units =list(set(major_units).union(set(degree_units)))
		
			
		# filtered_unit_list : list of units available in the session
		filtered_unit_list = []
		
		for unit in all_core_units:

			try:
				unit_offerings = handbook.extract_unit_offering_of_unit(unit, year)
			except:
				continue
			# unit_offerings : ['s1 day', 's1 evening', 's3 day']
			# unit_offerings_session_codes : ['s1', 's1', 's3']
			# Just to know whether the unit is offered in the session or not

			unit_offerings_session_codes = [ unit_offering.split(" ")[0] for unit_offering in unit_offerings]
			
			for i in xrange(len(unit_offerings_session_codes)):
				unit_offerings_session_codes[i] = unit_offerings_session_codes[i].replace('d', 's').replace('e', 's')

			if session.lower() in unit_offerings_session_codes and unit not in student_units:
				filtered_unit_list.append(unit)

		
		for unit in filtered_unit_list:
			if unit in temp_complex_units.keys():
				pre_req = temp_complex_units[unit]
			else:
				pre_req = handbook.extract_pre_req_for_unit(unit, year)

			# Todo: Parse the grade  (P, Cr) as well
			pre_req = pre_req.replace("(P)", "").replace("(Cr)", "")
			
			for complex_req in remaining_requirements:
				pre_req = pre_req.replace(complex_req, 'True')

			
			#print unit, ' : ' , pre_req
			
			#print 'pre_req: ', pre_req
			
			if not pre_req and unit not in final_available_units:
				final_available_units.append(unit)
				continue
			
			pre_req_tree = parser.parse_string(pre_req)
			
			evaluate_result = ev.evaluate_prerequisite(pre_req_tree, student_units)
		
			if evaluate_result and unit not in final_available_units:
				final_available_units.append(unit)

		return final_available_units


	def get_available_units_for_entire_degree(self, year='2011', session='S1'):
		"""
		Iterates over all sessions in three years for Bachelor and recommends the core units along with session
		Output {
			    "2011": [
					        { "s1": [ "COMP115" ] },
					        { "s2": [ "COMP125", "DMTH137", "ISYS114" ] }
			    		],
			    "2012": [
					        { "s1": [ "DMTH237" ] },
					        { "s2": [ "COMP255", "ISYS224" ] }
					    ],
			    "2013": [
					        { "s1": [ "COMP355" ] },
					        { "s2": [] }
					    ]
				}
		"""
		handbook = Handbook()

		student_units = aggregate_student_units = []
		final_available_units = {}
		if session.lower() == 's1':
			toggle = itertools.cycle(['s1', 's2']).next
		elif session.lower() == 's2':
			toggle = itertools.cycle(['s2', 's1']).next
		#student_units = ['COMP125', 'COMP115', 'COMP165', 'MAS111', 'INFO111', 'DMTH237']

		degree_requirements = handbook.extract_degree_requirements(self.degree_code, year)
		major_requirements = handbook.extract_major_req_units(self.major_code, year)

		major_units = [ unit for unit in major_requirements if len(unit.split(" ")) == 1 ]
		degree_units = [ unit for unit in degree_requirements if len(unit.split(" ")) == 1 ]
		remaining_requirements = list(set(degree_requirements).union(set(major_requirements)) - set(major_units).union(set(degree_units)) )
		#print 'remaining_requirements: ', remaining_requirements
		# print 'major_units: ', major_units
		all_core_units =list(set(major_units).union(set(degree_units)))
		


		#print 'Available Units'
		final_available_units[year] = []
		for i in range(0,6):

			additional_units = []
			session = toggle()

			student_units = self.get_available_units(year, session, aggregate_student_units, all_core_units, remaining_requirements)
			if len(student_units) < 4:
				additional_units = [ 'True '] * ( 4 - len(student_units))
			else:
				additional_units = []
			aggregate_student_units += student_units + additional_units
			
			temp_dict = {}
			temp_dict[session] = student_units

			final_available_units[year].append(temp_dict)
			
			#print "Session: ", year, " ",  session
			#print "Available Units: ", student_units
			#print 'aggregate_student_units: ', aggregate_student_units

			if session.lower() == "s2":
				year = str(int(year) + 1)
				final_available_units[year] = []
		
		if not final_available_units[year]:
			final_available_units.pop(year, None)
		
		return final_available_units

if __name__ == '__main__':
	dp = Degree_Planner('BIT', 'SOT01')
	handbook = Handbook()
	final = dp.get_available_units_for_entire_degree()
	print json.dumps(final, sort_keys=True, indent=4)

	#print "Session: ", year, " ",  session

	#s1_units = dp.get_available_units('2011', 's2', ['COMP115'])
	#print s1_units
	

	


