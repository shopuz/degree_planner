from parser import *
from handbook import *
from datetime import date
import math
import itertools
from compiler.ast import flatten
import random

class Degree_Planner():

	def __init__(self, degree_code, major_code, year, session):
		self.degree_code = degree_code
		self.major_code = major_code
		self.year = year
		self.session = session.lower()
		self.remaining_requirements = []
	
	def filter_units_by_offerings(self, units, student_units):
		# filtered_unit_list : list of units available in the session
		filtered_unit_list = []
		
		for unit in units:

			try:
				unit_offerings = handbook.extract_unit_offering_of_unit(unit, self.year)
			except:
				continue
			# unit_offerings : ['s1 day', 's1 evening', 's3 day']
			# unit_offerings_session_codes : ['s1', 's1', 's3']
			# Just to know whether the unit is offered in the session or not

			unit_offerings_session_codes = [ unit_offering.split(" ")[0] for unit_offering in unit_offerings]
			
			for i in xrange(len(unit_offerings_session_codes)):
				unit_offerings_session_codes[i] = unit_offerings_session_codes[i].replace('d', 's').replace('e', 's')

			if self.session in unit_offerings_session_codes and unit not in student_units:
				filtered_unit_list.append(unit)
		return filtered_unit_list

	def get_available_units(self, student_units=[], 
								  all_core_units=None, remaining_requirements=None):
		"""
		Get the available units in the given year and session.
		Output: list type:
				['COMP115']
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
		# all_core_units might be empty list passed from other function which is a desired
		# if this function is called directly from main, then execute the following
		if not isinstance(all_core_units, list):
			degree_requirements = handbook.extract_degree_requirements(self.degree_code, self.year)
			major_requirements = handbook.extract_major_req_units(self.major_code, self.year)

			major_units = [ unit for unit in major_requirements if len(unit.split(" ")) == 1 ]
			degree_units = [ unit for unit in degree_requirements if len(unit.split(" ")) == 1 ]
			remaining_requirements = list(set(degree_requirements).union(set(major_requirements)) - set(major_units).union(set(degree_units)) )
			all_core_units =list(set(major_units).union(set(degree_units)))
		
			
		# filtered_unit_list : list of units available in the session
		filtered_unit_list = []
		
		for unit in all_core_units:

			try:
				unit_offerings = handbook.extract_unit_offering_of_unit(unit, self.year)
			except:
				continue
			# unit_offerings : ['s1 day', 's1 evening', 's3 day']
			# unit_offerings_session_codes : ['s1', 's1', 's3']
			# Just to know whether the unit is offered in the session or not

			unit_offerings_session_codes = [ unit_offering.split(" ")[0] for unit_offering in unit_offerings]
			
			for i in xrange(len(unit_offerings_session_codes)):
				unit_offerings_session_codes[i] = unit_offerings_session_codes[i].replace('d', 's').replace('e', 's')

			if self.session in unit_offerings_session_codes and unit not in student_units:
				filtered_unit_list.append(unit)

		
		for unit in filtered_unit_list:
			if unit in temp_complex_units.keys():
				pre_req = temp_complex_units[unit]
			else:
				pre_req = handbook.extract_pre_req_for_unit(unit, self.year)

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


	def get_available_units_for_entire_degree(self):
		"""
		Iterates over all sessions in three years for Bachelor and recommends the core units along with session
		Output : dictionary type
				{
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
		if self.session == 's1':
			toggle = itertools.cycle(['s1', 's2']).next
		elif self.session == 's2':
			toggle = itertools.cycle(['s2', 's1']).next
		#student_units = ['COMP125', 'COMP115', 'COMP165', 'MAS111', 'INFO111', 'DMTH237']

		degree_requirements = handbook.extract_degree_req_units(self.degree_code, self.year)
		major_requirements = handbook.extract_major_requirements(self.major_code, self.year)

		print 'degree_requirements: ', degree_requirements

		major_units = [ unit for unit in major_requirements if len(unit.split(" ")) == 1 ]
		degree_units = [ unit for unit in degree_requirements if len(unit.split(" ")) == 1 ]
		remaining_requirements = list(set(degree_requirements).union(set(major_requirements)) - set(major_units).union(set(degree_units)) )
		#print 'remaining_requirements: ', remaining_requirements
		#print 'major_units: ', major_units
		self.remaining_requirements = remaining_requirements

		all_core_units =list(set(major_units).union(set(degree_units)))
		


		#print 'Available Units'
		final_available_units[self.year] = []
		for i in range(0,6):

			additional_units = []
			self.session = toggle()

			student_units = self.get_available_units(aggregate_student_units, all_core_units, remaining_requirements)
			if len(student_units) < 4:
				additional_units = [ 'True '] * ( 4 - len(student_units))
			else:
				additional_units = []
			aggregate_student_units += student_units + additional_units
			
			temp_dict = {}
			temp_dict[self.session] = student_units

			final_available_units[self.year].append(temp_dict)
			

			all_core_units = list(set(all_core_units) - set(aggregate_student_units))


			if self.session == "s2":
				self.year = str(int(self.year) + 1)
				final_available_units[self.year] = []
		
		if not final_available_units[self.year]:
			final_available_units.pop(self.year, None)
		
		# satisfy_remaining_requirements(remaining_requirements, final_available_units)

		return final_available_units

	def satisfy_remaining_requirements(self, final_available_units):
		# ['3cp from COMP units at 200 level', '9cp from COMP300-COMP350 or ISYS326', 'COMP225 or COMP229']
		parser = Prereq_Parser()
		evaluator = Evaluate_Prerequisite()
		negative_keywords = ['or', 'from']
		satisfiable_units = []
		student_units = ['COMP115', 'COMP125', 'DMTH137', 'DMTH237', 'ISYS114', 'ISYS224', 'ISYS326', 'COMP355']
		
		for req in self.remaining_requirements:
			pre_req_tree = parser.parse_string(req)
			pre_req_tree = list(set(flatten(pre_req_tree)))

			required_cp = evaluator.find_required_cp(pre_req_tree)
			all_unit_list = [pre_req for pre_req in pre_req_tree if 'cp' not in pre_req  and pre_req not in negative_keywords ]
			#print 'all_units: ', all_unit_list


			filtered_unit_list = self.filter_units_by_offerings(all_unit_list, student_units)
			#print 'filtered_unit_list: ', filtered_unit_list
			for unit in filtered_unit_list:
				pre_req = handbook.extract_pre_req_for_unit(unit, self.year)
				pre_req = pre_req.replace('(P)', '')
				pre_req_tree = parser.parse_string(pre_req)
				
				evaluate_result = evaluator.evaluate_prerequisite(pre_req_tree, student_units )
				if evaluate_result:
					satisfiable_units.append(unit)
					return satisfiable_units
	
	
	




if __name__ == '__main__':
	dp = Degree_Planner('BIT', 'SOT01', '2013', 's1')
	handbook = Handbook()
	final = dp.get_available_units_for_entire_degree()
	print json.dumps(final, sort_keys=True, indent=4)

	#print "Session: ", year, " ",  session

	#s1_units = dp.get_available_units(['COMP115'])
	#print s1_units
	#remaining_requirements = ['COMP225 or COMP229']
	#final_available_units = {'2011': [{'s1': ['COMP115']}, {'s2': ['COMP125', 'DMTH137', 'ISYS114']}], '2013': [{'s1': ['COMP355']}, {'s2': []}], '2012': [{'s1': ['DMTH237']}, {'s2': ['COMP255', 'ISYS224']}]}
	#print dp.satisfy_remaining_requirements(remaining_requirements, final_available_units)
	


