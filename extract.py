"""
Author 	: Suren
Desc	: Get all the requirements for all the degrees from Handbook API

"""
import urllib, json

class DegreePlanner:
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
			individual_unit_url = "http://api.prod.handbook.mq.edu.au/Unit/JSON/%s/2014/9f9ef28dea630ae6311cc730207b2b59" % unit_code
			response = urllib.urlopen(individual_unit_url)
			unit_info = json.loads(response.read())
			#req_list.append({ unit_code: unit_info['Prerequisites'] })
			my_json = { unit_code : { "Prerequisites" : unit_info['Prerequisites'],
										"Corequisites" : unit_info['Corequisites'] 
									}}

			json.dump(my_json, outfile)
			outfile.write("\n")
		
		outfile.close()
			

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
		

		
		

	



if __name__ == "__main__":
	dp = DegreePlanner()
	
	#url = "http://api.prod.handbook.mq.edu.au/Degrees/JSON/2015/9f9ef28dea630ae6311cc730207b2b59"
	#extract_degree_req(url, 'DegreeRequirement.txt')

	#all_units_url = "http://api.prod.handbook.mq.edu.au/Units/JSON/2014/9f9ef28dea630ae6311cc730207b2b59"
	#dp.extract_pre_corequisite(all_units_url, 'UnitsRequisites.txt')

	specific_units = dp.extract_all_units_from_department("Department of Computing", 2014, 'undergraduate')
	if len(specific_units) != 0:
		print json.dumps(specific_units, indent=4)
		print "Total Number of Units: ", len(specific_units)
	else:
		print "Error: Please check level of units (undergraduate, postgraduate, research, graduate, all)"



