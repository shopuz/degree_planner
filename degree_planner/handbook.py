"""
Author 	: Suren
Desc	: Get all the requirements for all the degrees from Handbook API

"""
import urllib, json
from pyparsing import *
from datetime import date

# TOdo
# Write a function to get the level_code PGUnit, Unit, ResearchUnits etc from unit_code		
# Function to get the CP of a unit -- need it for cp_calculator

class Handbook:
	def __init__(self):
		self.word = Word(alphas)
		self.nums = Word(nums)
		self.wn = self.word + self.nums
		self.year = date.today().year

		self.level_code_dict = {
								'undergraduate' : 	'Units',
								'postgraduate'	:	'PGUnits',
								'research'		:	'ResearchUnits',
								'graduate'		:	'GradUnits'
								}

	
	def get_level_code_from_unit(self, unit_code):
		"""
		Find the level_code (Unit, PGUnit) from unit_code for Handbook API URL
		Example: COMP115 -> Unit, ITEC810 -> PGUnit
		"""
		unit_number = int(self.wn.parseString(unit_code).asList()[1])
		if unit_number <= 499:
			level_code = 'Unit'
		else:
			level_code = 'PGUnit'

		return level_code

	def extract_all_degrees(self, year):
		"""
		Extract all the degrees of the year
		Output: { 	'AssocDegIT' : 'Associate Degree in Information Technology',
					'BActStud'	 :	'Bachelor of Actuarial Studies'
				}
		"""
		url = 'http://api.prod.handbook.mq.edu.au/Degrees/JSON/%s/9f9ef28dea630ae6311cc730207b2b59' % year
		response = urllib.urlopen(url)
		all_degrees_info = json.loads(response.read())
		all_degrees = {}
		for degree in all_degrees_info:
			all_degrees[degree['Code']] = degree['Name']

		return all_degrees

	def extract_all_majors_of_degree(self, degree_code, year):
		"""
		Extract all the majors of a particular degree
		"""
		all_majors = {}
		url = 'http://api.prod.handbook.mq.edu.au/Degree/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59' % (degree_code, year)
		response = urllib.urlopen(url)
		degree_info = json.loads(response.read())
		for key in degree_info['QualifyingMajors'].keys():
			all_majors_info = degree_info['QualifyingMajors'][key]
			for major in all_majors_info:
				all_majors[major['Code']] = major['Name']
		
		return all_majors

	def extract_degree_req(self, url, filename):
		"""
		Extracts the list of all the degree requirements in a year. Degree Code is not mentioned in the output file
		url : list of all the degrees in a particular year
		Return: Output File with the following information:
				Minimum number of credit points for the degree 
				Minimum number of credit points at 200 level or above
		"""
		response = urllib.urlopen(url)
		degrees = json.loads(response.read())
		DegreeReq_list = []
		for degree in degrees:
			degree_id = degree['Id']
			individual_degree_url = "http://api.prod.handbook.mq.edu.au/Degree/JSON/%s/2015/9f9ef28dea630ae6311cc730207b2b59" % degree_id
			response = urllib.urlopen(individual_degree_url)
			degree_info = json.loads(response.read())
			# print degree_info
			for req in degree_info['GenReqs']:
				if req['DegreeReq'] not in DegreeReq_list:
					DegreeReq_list.append(req['DegreeReq'])

		outfile = open(filename, 'w')
		outfile.write("\n".join(DegreeReq_list))


	def extract_pre_corequisite(self, url, filename):
		"""
		Extracts all the prerequisites of all the units in a year.
		url : list of all units (undergrad/postgrad)
		Return: Output File with the following information:
				{"ABEC121": "Admission to BTeach(ECS)"}
				{"ABEC150": "Admission to BTeach(ECS)"}

		"""
		response = urllib.urlopen(url)
		units = json.loads(response.read())
		
		outfile = open(filename, 'w')
		for unit in units:
			unit_code = unit['Code']
			individual_unit_url = "http://api.prod.handbook.mq.edu.au/PGUnit/JSON/%s/2014/9f9ef28dea630ae6311cc730207b2b59" % unit_code
			response = urllib.urlopen(individual_unit_url)
			unit_info = json.loads(response.read())
			#req_list.append({ unit_code: unit_info['Prerequisites'] })
			my_json = { unit_code : { "Prerequisites" : unit_info['Prerequisites'],
										"Corequisites" : unit_info['Corequisites'] 
									}}

			json.dump(my_json, outfile)
			outfile.write("\n")
		
		outfile.close()
	
	def extract_pre_req_for_unit(self, unit_code, year=None):
		"""
		Extract the prerequisite for a single unit
		Input : unit_code = COMP226
		Output: "COMP225(P) or COMP229(P) or COMP125(Cr)"
		"""
		if not year:
			year = self.year

		individual_unit_url = "http://api.prod.handbook.mq.edu.au/Unit/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59" % (unit_code, year)
		response = urllib.urlopen(individual_unit_url)
		unit_info = json.loads(response.read())
		#req_list.append({ unit_code: unit_info['Prerequisites'] })
		prereq = unit_info['Prerequisites'].encode('utf-8')
		return prereq
								

	

		
	def extract_all_units_from_department(self, department, year, type='undergraduate'):
		"""
		Extract all the units offered by the Department in a given year.
		Input : department = Department of Computing
				year = 2014
				type = undergraduate / postgraduate / research / graduate / all

		Return: List of Units
				[
				    {
				        "Code": "CBMS101",
				        "Name": "Foundations of Chemistry",
				        ...
				    }, ...
				]

		"""
		
		level_code  = self.level_code_dict[type]

		units_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, year)
		response = urllib.urlopen(units_url)
		units = json.loads(response.read())

		specific_units = [ unit for unit in units if unit['Department'].lower() == department.lower() ]
		
		return specific_units

	def extract_all_units_from_faculty(self, faculty, year, type='undergraduate'):
		"""
		Extract all the units offered by the Faculty in a given year.
		Input : faculty = Faculty of Science
				year = 2014
				type = undergraduate / postgraduate / research / graduate / all

		Return: List of Units
				[
				    {
				        "Code": "CBMS101",
				        "Name": "Foundations of Chemistry",
				        ...
				    }, ...
				]

		"""
		
		level_code  = self.level_code_dict[type]

		units_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, year)
		response = urllib.urlopen(units_url)
		units = json.loads(response.read())

		specific_units = [ unit for unit in units if unit['Faculty'].lower() == faculty.lower() ]
		
		return specific_units
	

	def extract_all_units(self, year, type='undergraduate'):
		"""
		Extract all the units in a given year.
		Input : year = 2014
				type = undergraduate / postgraduate / research / graduate / all

		Return: List of Units
				[ 'COMP115', 'COMP125', ''... ]
				
		"""
		# ToDO: get all the units

		level_code  = self.level_code_dict[type]
			
		units_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, year)
		response = urllib.urlopen(units_url)
		units = json.loads(response.read())

		all_unit_codes = [ unit['Code'] for unit in units]
		
		return all_unit_codes

	def extract_all_units_of_level(self, year, level, type='undergraduate'):
		"""
		Extract all the units of a particular level in a given year.
		Input : year = 2014
				type = undergraduate / postgraduate / research / graduate / all

		Return: List of Units
				[ 'COMP115', 'COMP125', ''... ]
				
		"""
		# ToDO: get all the units

		level_code  = self.level_code_dict[type]
			
		units_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, year)
		response = urllib.urlopen(units_url)
		units = json.loads(response.read())

		all_unit_codes = [ unit['Code'].encode('utf-8') for unit in units if int(self.wn.parseString(unit['Code'])[1]) > level and int(self.wn.parseString(unit['Code'])[1]) <= level + 99 ]
		
		return all_unit_codes
		

	def extract_unit_offering_of_unit(self, unit_code, year, type="undergraduate"):
		"""
		Extract the unit offering information about a unit
		Output: ['s1 day', 's1 evening', 's3 day']
		"""
		# Todo: Get level code 'unit/ pgunit/ researchunit'
		level_code = 'Unit'
		unit_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, unit_code, year)
		response = urllib.urlopen(unit_url)
		unit_info = json.loads(response.read())
		unit_offerings = []
		if 'UnitOfferings' not in unit_info.keys():
			return []

		for unit_offering in unit_info['UnitOfferings']:
			unit_offerings.append(unit_offering['code'].encode('utf-8').lower())

		return unit_offerings

	def filter_units_by_offering(self, unit_list, year, session):
		"""
		Filter the unit_list by looking into its offerings
		"""
		filtered_unit_list = []
		for unit in unit_list:
			print 'Unit: ', unit
			unit_offerings = self.extract_unit_offering_of_unit(unit, year)
			unit_offerings_session_codes = [ unit_offering.split(" ")[0].replace('d', 's').replace('e', 's') for unit_offering in unit_offerings]
			if session in unit_offerings_session_codes:
				filtered_unit_list.append(unit)
		return filtered_unit_list

	def extract_unit_designation(self, unit_code, year=None):
		"""
		Find the designation of a unit whether its IT, Science, Management etc
		Input: extract_unit_designation('COMP115', '2014')
		Output: ['Engineering', 'Information Technology', 'Science', 'Technology']
		"""

		if not year:
			year = self.year

		level_code = self.get_level_code_from_unit(unit_code)
		unit_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, unit_code, year)
		response = urllib.urlopen(unit_url)
		unit_info = json.loads(response.read())
		unit_designations = [designation.encode('utf-8')  for designation in unit_info['UnitDesignations'] ]
		
		return unit_designations
	
	def calculate_cp_of_designation(self, student_units, designation):
		"""
		Calculate the total cp obtained by the student given the units he/she had completed
		"""
		filtered_unit_list = []
		for unit in student_units:
			unit_designations = self.extract_unit_designation(unit)
			if designation in unit_designations:
				filtered_unit_list.append(unit)
		
		# Todo: change 3 to actual cp depending on level
		total_cp = len(filtered_unit_list) * 3
		return total_cp



	def extract_all_units_of_type(self, unit_type='people'):
		""" 
		Extract the list of Planet, People or Participation Units depending on the type
		"""
		all_units = self.extract_all_units(2014)
		filtered_unit_list = []
		for unit in all_units:
			print unit
			unit_url = 'http://api.prod.handbook.mq.edu.au/Unit/JSON/%s/2014/9f9ef28dea630ae6311cc730207b2b59' % unit
			response = urllib.urlopen(unit_url)
			unit_info = json.loads(response.read())
			extracted_unit_type = unit_info['UnitType'].lower()
			if unit_type == extracted_unit_type:
				filtered_unit_list.append(unit.encode('utf-8'))

		return filtered_unit_list

	def parse_major_degree_requirements(self, requirements):
		"""
		Parses the requirements and extract all the units from either major or degree requirements
		Input: JSON data : 	major_info['Requirements'] 
							or 
							degree_info['Program'][0]['SpecificReqs']
		Output: List of all the units

		"""
		unit_list = []
		for level in requirements.keys():
			if not requirements[level]:
				continue

			for req_group in requirements[level]:
				# if major_req['level100'][0]['reqGp']['text']['type'] is null
				# Get unitprefix from reqs
				req_text_type = req_group['reqGp']['text']['type']
				if not req_text_type or req_text_type == 'eo' :
					for reqs in req_group['reqGp']['reqs']:
						unit = reqs['unitPrefix'] + reqs['unitNumber']
						if unit not in unit_list:
							unit_list.append(unit)
				else:

					for req in req_group['reqGp']['reqs']:
						if req['type'] == 'unit':
							unit = req['unitPrefix'] + req['unitNumber']
							if unit not in unit_list:
								unit_list.append(unit)
						elif req['type'] == 'prefixrange' or req['type'] == 'prefixlevel':
							for reqDetail in req['reqDetails']:
								unit = reqDetail['unitPrefix'] + reqDetail['unitNumber']
								if unit not in unit_list:
									unit_list.append(unit)

		unit_list = [unit.encode('utf-8') for unit in unit_list]
		return unit_list

	def extract_degree_req_units(self, degree_code='BIT', year='2014'):
		"""
		Get all the core units from degree requirements

		"""
		degree_url = 'http://api.prod.handbook.mq.edu.au/Degree/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59' % (degree_code, year)
		response = urllib.urlopen(degree_url)
		degree_info = json.loads(response.read())
		unit_list = []
		for program in degree_info['Program']:
			unit_list += self.parse_major_degree_requirements(program['SpecificReqs'])

		return unit_list

	def extract_major_req_units(self, major_code, year=None):
		"""
		Extract the requirement UnitList of a major

		Input : major_code = SOT01
		Output: ['COMP115', 'COMP125', 'DMTH137', 'COMP355', 'COMP329', 'COMP330', 'COMP332', 'COMP333', 
				'COMP334', 'COMP343', 'COMP344', 'COMP347', 'COMP348', 'COMP350', 'ISYS326', 'COMP255', 
				'DMTH237', 'COMP225', 'COMP229', 'COMP202', 'COMP226', 'COMP233', 'COMP247', 'COMP249', 'COMP260']
		"""
		if not year:
			year = self.year

		
		individual_major_url = "http://api.prod.handbook.mq.edu.au/Major/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59" % (major_code, year)

		response = urllib.urlopen(individual_major_url)
		major_info = json.loads(response.read())
		#req_list.append({ unit_code: unit_info['Prerequisites'] })
		unit_list = []
		major_req = major_info['Requirements']
		unit_list = self.parse_major_degree_requirements(major_req)
		return unit_list


	def parse_major_degree_requirements(self, requirements):
		unit_list = temp_unit_list = []
		temp_string = []
		for level in requirements.keys():
			if not requirements[level]:
				continue

			for req_group in requirements[level]:
				# if major_req['level100'][0]['reqGp']['text']['type'] is null
				# Get unitprefix from reqs
				req_text_type = req_group['reqGp']['text']['type']

				if not req_text_type :
					for reqs in req_group['reqGp']['reqs']:
						unit = reqs['unitPrefix'] + reqs['unitNumber']
						if unit not in unit_list:
							
							unit_list.append(unit)
				
				elif req_text_type == 'eo' :
					temp_unit_list = []
					for reqs in req_group['reqGp']['reqs']:

						unit = reqs['unitPrefix'] + reqs['unitNumber']
						
						temp_unit_list.append(unit)

					
					unit_list.append(' or '.join(temp_unit_list))
				
				else:

					for req in req_group['reqGp']['reqs']:
						if req['type'] == 'unit':
							unit = req['unitPrefix'] + req['unitNumber']
							if unit not in unit_list:
								temp_string.append(unit)
						elif req['type'] == 'prefixrange':
							#req_group['reqGp']['text']['label'] + ' ' + 
							req_string = req['unitPrefix'] +  req['unitLowerNum'] + '-' + req['unitPrefix'] + req['unitHigherNum']
							temp_string.append(req_string)
						elif req['type'] == 'prefixlevel':
							# 
							req_string = req_group['reqGp']['text']['label'] + ' ' +  req['unitPrefix'] + ' units at ' +  req['unitLevel'] + ' level'
							unit_list.append(req_string)
					if temp_string:
						if req_group['reqGp']['text']['type']:
							unit_list.append(req_group['reqGp']['text']['cp'] + 'cp from ' +  ' or '.join(temp_string))
						else:
							unit_list.append(' or '.join(temp_string))
						temp_string = []

		unit_list = [unit.encode('utf-8') for unit in unit_list]
		return unit_list

	def extract_major_requirements(self, major_code='SOT01', year='2014'):
		"""
			Extract the requirements of a major. It might be a list of units and strings
		"""

		individual_major_url = "http://api.prod.handbook.mq.edu.au/Major/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59" % (major_code, year)

		response = urllib.urlopen(individual_major_url)
		major_info = json.loads(response.read())
		requirements = major_info['Requirements']
		unit_list = self.parse_major_degree_requirements(requirements)
		return unit_list

	def extract_degree_requirements(self, degree_code='BIT', year='2014'):
		"""
		Extract the requirements of a degree. It might be a list of units and strings

		"""
		degree_url = 'http://api.prod.handbook.mq.edu.au/Degree/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59' % (degree_code, year)
		response = urllib.urlopen(degree_url)
		degree_info = json.loads(response.read())
		unit_list = []
		for program in degree_info['Program']:
			unit_list += self.parse_major_degree_requirements(program['SpecificReqs'])

		return unit_list

	def extract_general_requirements_of_degree(self, degree_code='BIT', year='2014'):
		"""
		Extract all the general requirements of the degree. 
		Output: {	'min_total_cp': 72,
					'min_200_above': 42,
					'min_300_above': 18,
					'min_designation_information_technology': 42,
					'foundation_units': 12
				}
		"""
		type1 = Literal("for the degree")
		type2 = Literal("for this degree")
		type3 = Literal("required for the degree")

		min_cp = Literal('Minimum number of credit points') + ZeroOrMore(type1 | type2 | type3)
		level = min_cp + Or([Literal('at'), Literal('required at')]) + Word(nums) + Literal('level') + ZeroOrMore(Literal('or above'))
		designation = Or([min_cp, level]) + ZeroOrMore(Literal('from') + OneOrMore(Word(alphas))) +  Or([Literal('designated'), Literal('designated units')]) + ZeroOrMore(Literal('as') +  OneOrMore(Word(alphas)))
		designation_completion = Literal('Completion of a') + Literal('designated') + Word(alphas) + Literal('unit') + ZeroOrMore(Literal('with a')) +ZeroOrMore(OneOrMore(Word(alphas))) + ZeroOrMore(Literal('prefix'))
		foundation = Literal('Completion of specified foundation units')
		complex_statement = ( foundation | designation | designation_completion| level | min_cp )

		negative_keywords = ['for the degree', 'for this degree', 'required for the degree', 'required for this degree', 'at', 'level', 'as', 'Completion of', 'a', 'unit', 'Completion of a']

		parsed_req = {}
		degree_url = 'http://api.prod.handbook.mq.edu.au/Degree/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59' % (degree_code, year)
		response = urllib.urlopen(degree_url)
		degree_info = json.loads(response.read())
		gen_reqs = degree_info['GenReqs']
		for req in gen_reqs:
			try:
				print 'req: ', req['DegreeReq']
				parsed_gen_req = complex_statement.parseString(req['DegreeReq']).asList()
				print 'parsed: ', parsed_gen_req
			except:
				continue
			
			parsed_gen_req = [gen_req for gen_req in parsed_gen_req if gen_req not in negative_keywords]
			final_parsed_gen_req = []
			for filtered_gen_req in parsed_gen_req:
				filtered_gen_req = filtered_gen_req.replace('Minimum number of credit points', 'min').replace('or above', 'above').replace('Completion of specified foundation units', 'foundation_units').replace('designated', 'designation').lower()
													
				final_parsed_gen_req.append(filtered_gen_req)
			if len(final_parsed_gen_req) == 1 and final_parsed_gen_req[0] == 'min':
				keyword = 'min_total_cp'
			else:
				keyword = '_'.join(final_parsed_gen_req)

			print "keyword: ", keyword
			print (req['DegreeReqCP'])
			if req['DegreeReqCP']:
				parsed_req[keyword] = int(req['DegreeReqCP'])
			
		return parsed_req


	def get_foundation_units(self, degree_code='BIT', year='2014'):
		"""
		Extract the foundation units of the degree

		"""
		degree_url = 'http://api.prod.handbook.mq.edu.au/Degree/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59' % (degree_code, year)
		response = urllib.urlopen(degree_url)
		degree_info = json.loads(response.read())
		unit_list = []
		for program in degree_info['Program']:
			if program['Type'] == 'Foundation':
				unit_list += self.parse_major_degree_requirements(program['SpecificReqs'])

		return unit_list		







if __name__ == "__main__":
	handbook = Handbook()
	
	#url = "http://api.prod.handbook.mq.edu.au/Degrees/JSON/2015/9f9ef28dea630ae6311cc730207b2b59"
	#extract_degree_req(url, 'DegreeRequirement.txt')

	#all_units_url = "http://api.prod.handbook.mq.edu.au/PGUnits/JSON/2014/9f9ef28dea630ae6311cc730207b2b59"
	#dp.extract_pre_corequisite(all_units_url, 'PGUnitsRequisites.txt')
	
	specific_units = handbook.extract_all_units_from_faculty("Faculty of Business and Economics", '2014', "undergraduate")
	for unit in specific_units:
		print unit['Code']

	#specific_units = dp.extract_all_units(2014, "undergraduate")
	'''
	if len(specific_units) != 0:
		print json.dumps(specific_units, indent=4)
		print "Total Number of Units: ", len(specific_units)
	else:
		print "Error: Please check level of units (undergraduate, postgraduate, research, graduate, all)"
	'''

	#major_units = handbook.extract_major_requirements('SOT01', '2014')
	#print 'result: '
	#print '-------'
	#print major_units

	#print hbook.extract_unit_offering_of_unit('COMP115', '2014')
	#print hbook.extract_unit_designation('COMP115', '2014')

	#student_units = ['COMP125', 'COMP115', 'MAS111', 'DMTH237', 'CBMS832']
	#print hbook.calculate_cp_of_designation(student_units, "Information Technology")
	
	#print handbook.extract_degree_req_units()
	#print handbook.extract_major_req_units()
	
	#print handbook.extract_general_requirements_of_degree('BIT', '2014')
	#print handbook.extract_all_majors_of_degree('BIT', '2014')
	#print handbook.extract_degree_requirements()
	#print handbook.extract_major_requirements('SOT01', '2014')
