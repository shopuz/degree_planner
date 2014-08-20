"""
Author 	: Suren
Desc	: Get all the requirements for all the degrees from Handbook API

"""
import urllib, json
from pyparsing import *
from datetime import date

class Handbook:
	def __init__(self):
		self.word = Word(alphas)
		self.nums = Word(nums)
		self.wn = self.word + self.nums
		self.year = date.today().year

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
								

	def extract_major_req_units(self, major_code, year=None):
		"""
		Extract the requirement UnitList of a major
		Input : major_code = SOT01
		Output: 
		"""
		if not year:
			year = self.year

		
		individual_major_url = "http://api.prod.handbook.mq.edu.au/Major/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59" % (major_code, year)

		response = urllib.urlopen(individual_major_url)
		major_info = json.loads(response.read())
		#req_list.append({ unit_code: unit_info['Prerequisites'] })
		unit_list = []
		major_req = major_info['Requirements']
		for level in major_req.keys():
			if not major_req[level]:
				continue

			for req_group in major_req[level]:
				# if major_req['level100'][0]['reqGp']['text']['type'] is null
				# Get unitprefix from reqs
				req_text_type = req_group['reqGp']['text']['type']
				if not req_text_type or req_text_type == 'eo' :
					for reqs in req_group['reqGp']['reqs']:
						unit_list.append(reqs['unitPrefix'] + reqs['unitNumber'])
				else:

					for req in req_group['reqGp']['reqs']:
						if req['type'] == 'unit':
							unit_list.append(req['unitPrefix'] + req['unitNumber'])
						elif req['type'] == 'prefixrange' or req['type'] == 'prefixlevel':
							for reqDetail in req['reqDetails']:
								unit_list.append(reqDetail['unitPrefix'] + reqDetail['unitNumber'])

		unit_list = [unit.encode('utf-8') for unit in unit_list]
		return unit_list

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
		# ToDO: get all the units

		if type == 'undergraduate':
			level_code = 'Units'
		elif type == 'postgraduate':
			level_code = 'PGUnits'
		elif type == 'research':
			level_code = 'ResearchUnits'
		elif type == 'graduate':
			level_code = 'GradUnits'
		else:
			return None
			
		units_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, year)
		response = urllib.urlopen(units_url)
		units = json.loads(response.read())

		specific_units = [ unit for unit in units if unit['Department'].lower() == department.lower() ]
		
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

		if type == 'undergraduate':
			level_code = 'Units'
		elif type == 'postgraduate':
			level_code = 'PGUnits'
		elif type == 'research':
			level_code = 'ResearchUnits'
		elif type == 'graduate':
			level_code = 'GradUnits'
		else:
			return None
			
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

		if type == 'undergraduate':
			level_code = 'Units'
		elif type == 'postgraduate':
			level_code = 'PGUnits'
		elif type == 'research':
			level_code = 'ResearchUnits'
		elif type == 'graduate':
			level_code = 'GradUnits'
		else:
			return None
			
		units_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, year)
		response = urllib.urlopen(units_url)
		units = json.loads(response.read())

		all_unit_codes = [ unit['Code'].encode('utf-8') for unit in units if int(self.wn.parseString(unit['Code'])[1]) > level and int(self.wn.parseString(unit['Code'])[1]) <= level + 99 ]
		
		return all_unit_codes
		

	def extract_unit_offering_of_unit(self, unit_code, year, type="undergraduate"):
		"""
		Extract the unit offering information about a unit
		Output: ['S1 Day', 'S1 Evening', 'S3 Day']
		"""
		# Todo: Get level code 'unit/ pgunit/ researchunit'
		level_code = 'Unit'
		unit_url = "http://api.prod.handbook.mq.edu.au/%s/JSON/%s/%s/9f9ef28dea630ae6311cc730207b2b59" % (level_code, unit_code, year)
		response = urllib.urlopen(unit_url)
		unit_info = json.loads(response.read())
		unit_offerings = []
		for unit_offering in unit_info['UnitOfferings']:
			unit_offerings.append(unit_offering['code'].encode('utf-8').lower())

		return unit_offerings




if __name__ == "__main__":
	hbook = Handbook()
	
	#url = "http://api.prod.handbook.mq.edu.au/Degrees/JSON/2015/9f9ef28dea630ae6311cc730207b2b59"
	#extract_degree_req(url, 'DegreeRequirement.txt')

	#all_units_url = "http://api.prod.handbook.mq.edu.au/PGUnits/JSON/2014/9f9ef28dea630ae6311cc730207b2b59"
	#dp.extract_pre_corequisite(all_units_url, 'PGUnitsRequisites.txt')
	
	#specific_units = dp.extract_all_units_from_department("Department of Computing", 2014, "undergraduate")
	#specific_units = dp.extract_all_units(2014, "undergraduate")
	'''
	if len(specific_units) != 0:
		print json.dumps(specific_units, indent=4)
		print "Total Number of Units: ", len(specific_units)
	else:
		print "Error: Please check level of units (undergraduate, postgraduate, research, graduate, all)"
	'''

	#major_units = hbook.extract_major_req_units('SOT01', '2014')
	#print major_units

	print hbook.extract_unit_offering_of_unit('COMP115', '2014')
	

