from prereq_parser import *
from extract import *
from datetime import date

class Degree_Planner():

	def __init__(self, degree_code=None, major_code=None):
		self.degree_code = degree_code
		self.major_code = major_code
		


	def available_units(self, session="S1", student_units=None):
		# 1. Get all units from Major Requirements
		# 2. Filter the list with current unit offerings
		# 3. Get prereq of each unit
		# 4. Parse and Evaluate each prereq
		# 5. Finally prepare the list of all units which passed the prereq evaluation




if __name__ == '__main__':
