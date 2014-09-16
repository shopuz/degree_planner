from degree_parser import *
from handbook import *
from datetime import date
import math
import itertools
from compiler.ast import flatten
import random

class Degree_Planner():

	def __init__(self, degree_code='', major_code='', year='', session=''):
		self.degree_code = degree_code
		self.major_code = major_code
		self.year = year
		self.session = session.lower()
		self.remaining_requirements = []
		self.gen_degree_req = {}
		self.degree_req_units = []
		self.major_req_units = []
		self.planned_student_units = []
		self.planned_student_units_json = {}
		self.planet_units = ['ACCG260', 'AHIS230', 'ANTH106', 'ASTR170', 'ASTR178', 'BBE100', 'BIOL108', 'BIOL260', 'BIOL261', 'BUSL100', 'CBMS123', 'ECON131', 'EDUC108', 'EDUC261', 'ENV200', 'ENVE214', 'ENVE237', 'ENVG262', 'GEOS112', 'GEOS126', 'GEOS204', 'ISYS100', 'LEX102', 'LING337', 'MATH109', 'MATH123', 'MSM310', 'PHL260', 'PHYS159', 'PHYS242', 'SCOM100', 'SOC254', 'SPED102', 'STAT170', 'STAT175']
		self.people_units = ['ABST100', 'ACBE100', 'ACSC100', 'ACSH100', 'AFAS300', 'AHIS120', 'AHIS140', 'AHMG101', 'ANTH151', 'ANTH202', 'ANTH305', 'ASN101', 'BBA340', 'BCM310', 'COGS201', 'COGS202', 'CUL260', 'CUL399', 'DANC101', 'ECH113', 'ECH126', 'ECH130', 'ECHL213', 'ENGL108', 'ENVG111', 'EUL101', 'FBE204', 'GEN110', 'GEOS251', 'HRM107', 'INTS204', 'LEX101', 'LING109', 'LING120', 'LING248', 'LING290', 'LING332', 'LING397', 'MAS214', 'MHIS115', 'MHIS202', 'MHIS211', 'MKTG127', 'MKTG309', 'MUS205', 'PHL132', 'PHL137', 'POL107', 'POL108', 'POL304', 'PSY250', 'PSY350', 'SOC175', 'SOC182', 'SOC295', 'SOC297', 'SOC315']
		self.comp_units = ['COMP111','COMP115','COMP125','COMP188','COMP202','COMP225','COMP226','COMP229','COMP233','COMP247','COMP249','COMP255','COMP260','COMP329','COMP330','COMP332','COMP333','COMP334','COMP343','COMP344','COMP347','COMP348','COMP350','COMP352','COMP355','COMP365','COMP388','ISYS100','ISYS104','ISYS114','ISYS200','ISYS224','ISYS254','ISYS301','ISYS302','ISYS303','ISYS304','ISYS326','ISYS355','ISYS358','ISYS360']
		self.bus_eco_units = ['ACCG100','ACCG101','ACCG106','ACCG200','ACCG224','ACCG250','ACCG251','ACCG260','ACCG301','ACCG308','ACCG315','ACCG326','ACCG330','ACCG340','ACCG350','ACCG355','ACCG358','ACCG399','ACST101','ACST152','ACST201','ACST202','ACST212','ACST255','ACST306','ACST307','ACST315','ACST355','ACST356','ACST357','ACST358','ACST359','ACST402','ACST403','ACST404','AFAS300','AFIN100','AFIN252','AFIN253','AFIN310','AFIN315','AFIN328','AFIN329','AFIN331','AFIN341','AFIN352','AFIN353','AFIN450','BBA102','BBA111','BBA220','BBA280','BBA310','BBA315','BBA320','BBA340','BBA350','BBA360','BUS201','BUS202','BUS301','BUS303','BUS304','BUS305','BUSL100','BUSL201','BUSL204','BUSL250','BUSL301','BUSL315','BUSL320','BUSL377','BUSL388','DEM355','ECON110','ECON111','ECON131','ECON203','ECON204','ECON214','ECON215','ECON232','ECON241','ECON244','ECON303','ECON309','ECON311','ECON315','ECON333','ECON334','ECON335','ECON336','ECON350','ECON356','ECON359','ECON360','ECON361','ECON394','FBE204','FOBE200','FOBE201','FOBE300','FOBE301','FOBE302','HRM107','HRM201','HRM222','HRM250','HRM300','HRM307','HRM317','HRM328','MGMT255','MGMT256','MGMT300','MGMT315','MKTG101','MKTG127','MKTG202','MKTG203','MKTG204','MKTG205','MKTG207','MKTG208','MKTG209','MKTG216','MKTG303','MKTG304','MKTG305','MKTG306','MKTG307','MKTG308','MKTG309','MKTG310','MKTG311','MKTG350']

		self.units_2014_s1 = ['AHIS230', 'ANTH106', 'ASTR170', 'BBE100', 'BIOL108', 'BUSL100', 'ECON131', 'EDUC108', 'EDUC261', 'ENVG262', 'GEOS112', 'GEOS204', 'ISYS100', 'LING337', 'DMTH237', 'MATH109', 'MATH123', 'SCOM100', 'STAT170', 'STAT175', 'ABST100', 'ACBE100', 'ACSC100', 'ACSH100', 'AFAS300', 'AHMG101', 'ANTH305', 'ASN101', 'BBA340', 'BCM310', 'COGS201', 'DANC101', 'ECH113', 'ECH126', 'ENVG111', 'FBE204', 'GEN110', 'GEOS251', 'HRM107', 'LEX101', 'LING109', 'LING120', 'LING248', 'LING332', 'LING397', 'MHIS115', 'MHIS211', 'MKTG127', 'MKTG309', 'MUS205', 'PHL132', 'PHL137', 'POL108', 'POL304', 'PSY250', 'SOC175', 'SOC295', 'SOC297', 'COMP115', 'COMP125', 'COMP188', 'COMP225', 'COMP247', 'COMP249', 'COMP260', 'COMP330', 'COMP343', 'COMP348', 'COMP350', 'COMP352', 'COMP355', 'COMP388', 'ISYS100', 'ISYS104', 'ISYS254', 'ISYS302', 'ISYS326', 'ISYS355', 'ISYS358', 'ISYS360', 'ACCG100', 'ACCG101', 'ACCG106', 'ACCG200', 'ACCG224', 'ACCG250', 'ACCG301', 'ACCG308', 'ACCG315', 'ACCG326', 'ACCG330', 'ACCG340', 'ACCG350', 'ACCG358', 'ACCG399', 'ACST101', 'ACST152', 'ACST202', 'ACST306', 'ACST315', 'ACST356', 'ACST358', 'ACST402', 'AFAS300', 'AFIN252', 'AFIN253', 'AFIN310', 'AFIN315', 'AFIN329', 'AFIN353', 'BBA102', 'BBA111', 'BBA280', 'BBA310', 'BBA315', 'BBA340', 'BBA350', 'BBA360', 'BUS201', 'BUS301', 'BUSL100', 'BUSL201', 'BUSL250', 'BUSL301', 'BUSL320', 'BUSL377', 'DEM355', 'ECON110', 'ECON111', 'ECON131', 'ECON203', 'ECON204', 'ECON214', 'ECON241', 'ECON303', 'ECON309', 'ECON315', 'ECON333', 'ECON334', 'ECON335', 'ECON336', 'ECON350', 'ECON356', 'ECON361', 'FBE204', 'FOBE200', 'FOBE300', 'FOBE301', 'FOBE302', 'HRM107', 'HRM201', 'HRM222', 'HRM250', 'HRM300', 'HRM307', 'HRM328', 'MGMT255', 'MGMT256', 'MGMT315', 'MKTG101', 'MKTG127', 'MKTG202', 'MKTG203', 'MKTG204', 'MKTG207', 'MKTG208', 'MKTG209', 'MKTG216', 'MKTG303', 'MKTG304', 'MKTG306', 'MKTG308', 'MKTG309', 'MKTG311', 'MAS110', 'MAS240', 'MECO319']
		self.units_2014_s2 = ['ACCG260', 'ASTR178', 'BIOL108', 'BIOL260', 'BIOL261', 'CBMS123', 'ECON131', 'ENV200', 'ENVE214', 'ENVE237', 'GEOS126', 'ISYS100', 'DMTH137', 'LEX102', 'MATH123', 'MSM310', 'PHL260', 'PHYS159', 'PHYS242', 'SOC254', 'SPED102', 'STAT170', 'STAT175', 'ABST100', 'ACBE100', 'ACSC100', 'ACSH100', 'AFAS300', 'AHIS120', 'AHIS140', 'ANTH151', 'ANTH202', 'BBA340', 'COGS202', 'CUL260', 'CUL399', 'ECH130', 'ENGL108', 'EUL101', 'FBE204', 'HRM107', 'INTS204', 'LING290', 'MAS214', 'MKTG127', 'MKTG309', 'POL107', 'PSY350', 'SOC182', 'SOC315', 'COMP111', 'COMP125', 'COMP188', 'COMP202', 'COMP229', 'COMP255', 'COMP329', 'COMP332', 'COMP333', 'COMP344', 'COMP347', 'COMP350', 'COMP352', 'COMP355', 'COMP388', 'ISYS100', 'ISYS114', 'ISYS200', 'ISYS224', 'ISYS301', 'ISYS355', 'ISYS358', 'ACCG100', 'ACCG101', 'ACCG106', 'ACCG200', 'ACCG224', 'ACCG250', 'ACCG260', 'ACCG301', 'ACCG308', 'ACCG315', 'ACCG340', 'ACCG350', 'ACCG355', 'ACCG399', 'ACST101', 'ACST201', 'ACST212', 'ACST255', 'ACST307', 'ACST315', 'ACST355', 'ACST357', 'ACST359', 'ACST403', 'ACST404', 'AFAS300', 'AFIN100', 'AFIN252', 'AFIN253', 'AFIN310', 'AFIN315', 'AFIN328', 'AFIN329', 'AFIN352', 'BBA102', 'BBA111', 'BBA220', 'BBA320', 'BBA340', 'BBA350', 'BBA360', 'BUS201', 'BUS202', 'BUS303', 'BUS304', 'BUS305', 'BUSL204', 'BUSL250', 'BUSL301', 'BUSL315', 'BUSL320', 'BUSL388', 'ECON110', 'ECON111', 'ECON131', 'ECON203', 'ECON204', 'ECON215', 'ECON232', 'ECON241', 'ECON244', 'ECON311', 'ECON315', 'ECON334', 'ECON359', 'ECON360', 'ECON394', 'FBE204', 'FOBE200', 'FOBE201', 'FOBE300', 'FOBE302', 'HRM107', 'HRM250', 'HRM317', 'HRM328', 'MGMT300', 'MGMT315', 'MKTG101', 'MKTG127', 'MKTG202', 'MKTG203', 'MKTG204', 'MKTG205', 'MKTG208', 'MKTG209', 'MKTG303', 'MKTG304', 'MKTG307', 'MKTG309', 'MKTG310', 'MKTG350', 'MAS241', 'MAS110', 'MECO329']
		self.cached_pre_reqs = {'COGS201': '12cp', 'POL304': '39cp or (6cp in HIST or MHIS or POL units at 200 level including 3cp in POL)', 'COGS202': '12cp', 'HRM201': 'HRM107', 'ENVE237': '18cp(P)', 'ACST201': '15cp including ACST101(P)', 'MKTG350': '39cp', 'COMP225': '(COMP125(P) or COMP165(P)) and (3cp(P) from MATH132-MATH136 or DMTH137)', 'COMP226': 'COMP225(P) or COMP229(P) or COMP125(Cr)', 'ISYS304': '39cp and (COMP255(P) or ISYS254(P))', 'COMP229': 'COMP125(P) or COMP165(P)', 'ECON394': '27cp including [(ECON110 or ECON111 or BBA103) and (6cp at 200 level in units offered by the Faculty of Business and Economics)]', 'BBA360': 'Admission to BBA and (BBA103 or ECON110 or ECON111) and (BBA250 or HRM107) and BBA102 and (BBA216 or BUS201) and BBA350 and BUSL250', 'ISYS301': '39cp including [(ISYS254(P) or COMP255(P) or ISYS227(P) or COMP227(P)) and (6cp(P) in COMP or ISYS or ACCG or STAT or BUS or BBA units at 200 level)]', 'SOC182': '', 'ISYS303': '39cp including 6cp from (ISYS201(P) or ISYS224(P) or ISYS227(P) or ISYS254(P) or COMP224(P) or COMP225(P) or COMP227(P) or COMP229(P) or COMP255(P))', 'ANTH305': '39cp or admission to GDipArts', 'COMP348': '39cp and COMP249(P)', 'COMP347': '39cp and COMP247(P) and COMP125(P) and (MATH237(P) or DMTH237(P) or DMTH137(P) or ELEC240(P))', 'DANC101': '', 'COMP343': '39cp and (COMP125(P) or COMP165(P)) and (DMTH137(P) or MATH237(P) or DMTH237(P))', 'LING248': '12cp', 'BBA340': '42cp', 'ISYS224': 'ISYS114(P) or COMP114(P) or ISYS154(P) or COMP154(P)', 'BUS303': 'BUS301', 'BUS301': '39cp including BUS202', 'ECON360': '6cp at 200 level including (ECON200 or ECON201 or ECON203 or ECON204)', 'ASTR170': '', 'BUS305': '39cp', 'BUS304': '(39cp including BUS202) or (39cp and admission to BCom or BBA)', 'MKTG308': '(STAT122 or STAT170 or STAT171 or PSY122) and 6cp at 200 level including (MKTG202 or MKTG203 or MKTG204 or MKTG208 or MKTG210 or MKTG213 or BBA203 or BBA213)', 'ASTR178': '', 'ACST315': '48cp and permission of Executive Dean of Faculty', 'LING120': '', 'INTS204': '12cp', 'EUL101': '', 'FOBE302': '45cp', 'BUS201': 'BBA102 or admission to BeBus', 'ACST255': 'Admission to BActStud and ACST152(P) and ACST202(P) and STAT272(P) and GPA of 2.5', 'ECON241': '(STAT122 or STAT170 or STAT171 or PSY122) and (ECON110 or ECON111 or BBA103)', 'ECON315': '48cp and permission of Executive Dean of Faculty', 'LING397': '39cp', 'ENGL108': '', 'ENVG111': '', 'ECHL213': '12cp', 'ACCG326': '39cp including ACCG224(P)', 'MKTG208': 'MKTG101', 'MKTG209': 'MKTG101', 'BBA220': '24cp', 'COMP355': '39cp including ((COMP225(P) or COMP229(P)) and (COMP255(P) or COMP227(P) or ISYS227(P)))', 'AFIN100': '', 'MKTG203': 'MKTG101', 'COMP350': 'Permission of Executive Dean of Faculty', 'SOC295': '12cp', 'COMP352': '39cp and COMP260 and MECO319', 'ANTH151': '', 'ACST152': 'Admission to BActStud or (18cp and GPA of 3.25)', 'PHYS242': '12cp', 'ACST307': 'ACST306(P)', 'GEOS112': '', 'ECON311': '(ECON201 or ECON204) and (ECON232 or ECON241)', 'BUSL100': '', 'GEOS204': '12cp', 'MKTG202': 'MKTG101 and (STAT122 or STAT170 or STAT171 or PSY122)', 'ISYS326': '39cp including [(ISYS224(P) or COMP224(P)) and (ISYS254(P) or ISYS227(P) or ISYS201(P) or COMP225(P) or COMP227(P) or COMP229(P) or COMP255(P))]', 'ACCG251': '18cp including (ACCG101(P) or ACCG105(P))', 'ACST404': 'ACST306(P) and ACST355(P) and ACST357(P)', 'MKTG204': 'MKTG101', 'FOBE300': '39cp and permission of Executive Dean of Faculty', 'ACST402': 'ACST357(P) and ACST358(P)', 'ACST403': 'ACST402', 'MKTG101': '', 'ECON359': '6cp at 200 level including (ECON200 or ECON203)', 'ISYS200': '12cp including (ISYS100(P) or 6cp(P) in COMP or ISYS units at 100 level)', 'COMP202': 'COMP125\n', 'SOC297': '12cp', 'ACCG315': 'ACCG200(P) and ACCG224(P)', 'ENVG262': '12cp', 'AFAS300': '39cp', 'SOC315': '39cp or admission to GDipArts\n', 'BBA280': '', 'ECON356': 'ECON110 and ECON111 and 6cp at 200 level in units offered by the Faculty of Business and Economics', 'BIOL108': '', 'BBA310': '39cp including (BBA111 or HRM107)', 'COMP365': '39cp and COMP225(P) and (COMP227(P) or COMP255(P) or ISYS227(P)) and (admission to BCS or BBABCIS or BBABIT or BITLLB)', 'ECON361': '27cp including (6cp at 200 level including (ECON241 or STAT272))', 'ENV200': '12cp', 'MAS214': '15cp', 'ISYS302': '39cp including [(ISYS254(P) or COMP255(P) or ISYS227(P) or COMP227(P)) and (6cp(P) in COMP or ISYS or ACCG or STAT or BUS or BBA units at 200 level)]', 'HRM328': '48cp including (HRM201 and (HRM250 or BBA250))', 'ACCG330': '39cp including (ACCG201(P) or ACCG301(P))', 'ECON303': '6cp at 200 level including (ECON201 or ECON204)', 'AHMG101': '', 'ACST306': 'ACST202(P) and STAT272(P)', 'ACST101': '', 'ABST100': '', 'FOBE301': '45cp', 'ISYS355': '39cp including [(ISYS224(P) or COMP224(P)) and (ISYS254(P) or ISYS227(P) or COMP255(P) or COMP227(P)) and (ISYS254(P) or COMP229(P) or COMP249(P) or ISYS201(P))]', 'ACCG301': '39cp including ACCG200(P)', 'HRM250': 'HRM107', 'ISYS358': '39cp including (ISYS254(P) or COMP227(P) or ISYS227(P) or COMP255(P)) ', 'ACCG260': '18cp', 'ACCG308': '39cp including ACCG224(P)', 'MGMT256': '12cp including (DEM127 or HRM107)', 'MGMT255': '18cp', 'MKTG207': 'MKTG101', 'BBA111': '', 'AFIN252': '(ACCG100 or ACCG105 or ACCG106) and (ECON111 or BBA103) and (STAT170 or STAT171 or PSY122) and ACST101 and (24cp or GPA of 2.25)', 'AFIN253': '(ACCG100 or ACCG105 or ACCG106) and (ECON111 or BBA103) and (STAT170 or STAT171 or PSY122) and ACST101 and (24cp or GPA of 2.0)', 'LING337': '39cp', 'MKTG305': '(MKTG202 or MKTG203 or MKTG204 or MKTG208 or MKTG210 or MKTG213 or BBA203 or BBA213) and (STAT122 or STAT170 or STAT171 or PSY122)', 'ISYS114': '', 'MKTG307': '(STAT122 or STAT170 or STAT171 or PSY122) and 6cp at 200 level including (MKTG202 or MKTG203 or MKTG204 or MKTG208 or MKTG210 or MKTG213 or BBA203 or BBA213)', 'LING332': '39cp', 'MKTG309': '39cp', 'BUSL250': '12cp', 'BUSL204': '24cp', 'SOC175': '', 'PHL260': '12cp or admission to GDipArts', 'SCOM100': '', 'AFIN310': '3cp in ACST or AFIN units at 300 level', 'BCM310': '39cp and admission to BCM', 'AFIN315': '48cp and permission of Executive Dean of Faculty', 'ACCG250': '18cp including (ACCG100(P) or ACCG106(P))', 'COMP344': '39cp and (COMP224(P) or ISYS224(P)) and COMP249(P)', 'EDUC261': '12cp or EDUC105 or EDUC106 or EDUC107', 'MKTG205': 'MKTG101', 'MKTG216': '24cp', 'COMP332': '39cp and (COMP225(P) or COMP229(P))', 'ANTH106': '', 'MKTG310': 'MKTG101 and MKTG202 and MKTG203', 'FBE204': '24cp', 'ECON110': '', 'ECON111': '', 'MKTG127': '', 'MKTG311': 'MKTG202 and MKTG203 and (STAT122 or STAT170 or STAT171 or PSY122)', 'BBA350': 'Admission to BBA and MKTG101 and 6cp at 200 level including (ACCG200 or ACCG253 or AFIN253)', 'BUSL320': 'BUSL301 or 12cp in LAW units at 200 level', 'PSY350': '39cp', 'EDUC108': '', 'HRM317': '6cp at 200 level including (HRM201 or HRM207 or HRM250 or BBA250)', 'ISYS104': '', 'COMP260': 'COMP115 and (COMP111 or INFO111 or MAS111)', 'ISYS100': '', 'ACCG224': 'ACCG101(P)', 'ECON334': '27cp including (6cp at 200 level including (ECON241 or STAT272))', 'COMP388': '39cp and COMP188 and admission to BAdvSc and GPA of 2.75', 'ECON335': '6cp at 200 level including (ECON200 or ECON201 or ECON203 or ECON204)', 'GEOS126': '', 'MATH109': '', 'HRM307': '6cp at 200 level including (HRM201 or HRM207 or HRM250 or BBA250)', 'HRM300': '6cp at 200 level including (HRM201 or HRM222 or HRM250)', 'ECON336': '(STAT122 or STAT170 or STAT171 or PSY122) and 6cp at 200 level including (ECON200 or ECON201 or ECON203 or ECON204 or ECON214 or ECON215 or BBA204 or BBA214)', 'CBMS123': '', 'AFIN341': '39cp including AFIN252 and permission of Executive Dean of Faculty', 'BIOL261': '12cp', 'BIOL260': '12cp or admission to GCertBiotech', 'MHIS211': '12cp or (3cp in HIST or MHIS or POL units)', 'ACST358': 'ACST255(P) and STAT272(P)', 'ACST359': 'ACST358(P)', 'SPED102': '', 'ACST355': 'ACST358(P)', 'ACST356': '39cp including STAT272(P)', 'ACST357': 'ACST356(P) and STAT271(P)', 'PHYS159': '', 'COMP125': 'COMP115(P) or COMP155(P) or [admission to (BCom-ActStud or BActStud or BAdvSc or Advanced Program BSc) or (an equivalent admission rank or aggregate)]', 'HRM222': '12cp', 'AHIS120': '', 'BBA315': '39cp including (STAT170 or STAT171 or MKTG216)', 'LING290': '12cp', 'FOBE201': '18cp and permission of Executive Dean of Faculty', 'FOBE200': '24cp and permission of Executive Dean of Faculty', 'ACCG200': 'ACCG101 or ACCG105(P) or ACCG106(P)', 'SOC254': '12cp', 'BBA102': '', 'AFIN331': '39cp including AFIN252 and permission of Executive Dean of Faculty', 'MUS205': '12cp or admission to GCertArts', 'BUSL315': 'BUSL201 and (BUSL250 or LAW204)', 'MKTG303': 'MKTG202 and MKTG203 and (ACCG100 or ACCG105 or ACCG106 or MMCS105) and (BBA103 or ECON110 or ECON111 or admission to BMktgMedia) and 6cp in MKTG units at 300 level', 'MKTG306': '(STAT122 or STAT170 or STAT171 or PSY122) and 6cp at 200 level including (MKTG202 or MKTG203 or MKTG204 or MKTG208 or MKTG210 or MKTG213 or BBA203 or BBA213) ', 'COMP255': '18cp including (COMP115(P) or COMP155(P))', 'MHIS115': '', 'MGMT300': '39cp including (6cp in BUS or HRM or MKTG units at 200 level)\n', 'ACSC100': '', 'ECH130': '', 'POL107': '', 'ACSH100': '', 'ECON215': '15cp including (BBA103 or ECON111)', 'ECON214': '15cp including (BBA103 or ECON110)', 'ACCG100': '(Admission to BCom or BCom-Accg or BCom-ProfAccg or BAppFin or BComBA-Psych) or (an equivalent admission rank or aggregate) or (12cp and GPA of 2.0)', 'ECON350': '6cp at 200 level including (ECON200 or ECON201 or ECON203 or ECON204)', 'POL108': '', 'CUL260': '12cp', 'MGMT315': '48cp and permission of Executive Dean of Faculty', 'ECON232': 'ECON141 or ECON241 or STAT272', 'MHIS202': '12cp or (3cp in HIST or MHIS or POL units)', 'ECON131': '', 'ASN101': '', 'ACCG358': '39cp including (ACCG250 or ACCG251)', 'DEM355': '39cp including DEM127', 'ACCG355': '39cp including (ACCG250(P) or ACCG251(P) or ISYS104)', 'AHIS230': '12cp', 'ISYS360': '39cp', 'ACCG350': '39cp including (ACCG253(P) or ACCG252(P) or AFIN252(P) or AFIN253(P))', 'ECON333': '6cp at 200 level including (ECON232 or ECON233 or ECON334)', 'COMP247': '3cp(P) from COMP or ISYS units at 100 level', 'ACCG106': '', 'COMP329': '39cp and COMP125(P) or COMP249(P)', 'ACCG101': 'ACCG100(P) or ACCG105(P)', 'ECON244': 'ECON110 or ECON111', 'ENVE214': '12cp(P)', 'COMP249': '(COMP115(P) or COMP155(P)) and (ISYS114(P) or ISYS154(P))', 'GEOS251': '12cp', 'BUSL201': '12cp or BUSL100', 'LEX102': '', 'MSM310': 'Permission of Executive Dean of Faculty', 'LEX101': '', 'BBA320': '27cp including [(ECON110 or ECON111) and (6cp in ACCG or ACST or AFIN or ECON or FOBE or MGMT or MKTG units at 200 level)]', 'AFIN328': '39cp including (ACCG252 or AFIN252)', 'COMP115': '', 'ANTH202': 'ANTH150 or 12cp or (admission to GDipArts or BHlth)', 'COMP188': 'Admission to BAdvSc', 'COMP111': '', 'BUS202': '(30cp including BUS201) or (30cp and admission to BeBus)', 'ECON203': '15cp including ECON111 and (GPA of 2.0 or (admission to BEc or BCom or BAppFin or BActStud or BCom-Accg or BCom-ProfAccg or BBA))', 'ECON204': '15cp including ECON110 and (GPA of 2.0 or (admission to BEc or BCom or BAppFin or BActStud or BComAccg or BCom-ProfAccg or BBA))', 'ECH126': '', 'MATH123': '', 'BUSL388': '39cp', 'AFIN329': '6cp at 200 level including (ACCG252 or AFIN252)', 'ACST212': 'Admission to BActStud and STAT171(Cr)', 'ECON309': '39cp including (6cp at 200 level including (ECON200 or ECON203))', 'MKTG304': '(MKTG202 or MKTG203 or MKTG204 or MKTG208 or MKTG210 or MKTG213 or BBA203 or BBA213) and (STAT122 or STAT170 or STAT171 or PSY122)', 'GEN110': '', 'AFIN450': 'Permission of Executive Dean of Faculty', 'HRM107': '', 'ACCG340': '39cp including [(ACCG308(P) or ACCG310(P)) and (ACCG250(P) or ACCG251(P))]', 'PSY250': '24cp', 'COMP233': '18cp including (COMP115(P) or COMP155(P))', 'BUSL377': '39cp', 'PHL132': '', 'COMP333': '39cp and COMP225(P) and (DMTH237(P) or MATH237(P))', 'COMP330': '39cp and (COMP225(P) or COMP229(P)) and (DMTH137(P) or MATH237(P) or DMTH237(P))', 'AHIS140': '', 'BBE100': '', 'PHL137': '', 'COMP334': '39cp and COMP226(P) and (COMP225(P) or COMP229(P))', 'LING109': '', 'CUL399': '39cp', 'STAT175': '', 'ISYS254': 'ISYS114(P) or COMP114(P) or ISYS154(P) or COMP154(P)', 'STAT170': '', 'ACCG399': '(42cp including ACCG224(P)) or (42cp including ACCG315(P))', 'AFIN353': '39cp including (ACCG252 or AFIN252)', 'AFIN352': '39cp including (ACCG252 or AFIN252)', 'ACST202': 'ACST101(Cr) and MATH133(P) and GPA of 2.50', 'ACBE100': '', 'BUSL301': '39cp including BUSL250', 'ECH113': ''}

		# Todo: Remove this and make it more robust.
		# Can be done only after the parser can handle situations like admission / permission etc.
		self.temp_complex_units = {
								'COMP125' : 'COMP115(P) or COMP155(P)', 
								'COMP188' :	'', 
								'COMP247' :	'3cp from COMP or ISYS units at 100 level',
								'COMP365' : '39cp and COMP225(P) and (COMP227(P) or COMP255(P) or ISYS227(P))',
								'COMP388' :	'39cp and COMP188',
								'ISYS301' : '39cp',
								'ACCG100' : '',
								'ACCG399' :  '42cp including ACCG224 or ACCG315'

							}
	
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

		# TODO: REPLACE THE FOLLOWING WITH A CALL TO CACHE DB
		filtered_unit_list = []

		if self.session == 's1':
			filtered_unit_list = [ unit for unit in all_core_units if unit in self.units_2014_s1]
		elif self.session == 's2':
			filtered_unit_list = [ unit for unit in all_core_units if unit in self.units_2014_s2]


		print 'filtered_unit_list: ', filtered_unit_list

		
		"""
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

		"""

		for unit in filtered_unit_list:
			if unit in self.temp_complex_units.keys():
				pre_req = self.temp_complex_units[unit]
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

	def filter_units_by_prereq(self, student_units, units, year):
		handbook = Handbook()
		parser = Prereq_Parser()
		ev = Evaluate_Prerequisite()
		final_available_units = []

		
		for unit in units:
			print 'unit: ', unit
			if unit in self.temp_complex_units.keys():
				pre_req = self.temp_complex_units[unit]
			else:
				try:
					# TODO: Uncomment
					#pre_req = handbook.extract_pre_req_for_unit(unit, year)
					pre_req = self.cached_pre_reqs[unit]
				except:
					continue

			# Todo: Parse the grade  (P, Cr) as well
			pre_req = pre_req.replace("(P)", "").replace("(Cr)", "")
			
			if not pre_req and unit not in final_available_units:
				final_available_units.append(unit)
				continue
			
			try:
				pre_req_tree = parser.parse_string(pre_req)
			

				evaluate_result = ev.evaluate_prerequisite(pre_req_tree, student_units)
				print 'pre_req: ', pre_req
				print 'evaluate_result: ', evaluate_result
				if evaluate_result and unit not in final_available_units:
					final_available_units.append(unit)
			except:
				print unit,  ' : Prereq Parsing/Evaluation Error'
				continue
		



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
		
		if self.major_code:
			major_requirements = handbook.extract_major_requirements(self.major_code, self.year)
		else:
			major_requirements = []

		#print 'degree_requirements: ', degree_requirements

		major_units = [ unit for unit in major_requirements if len(unit.split(" ")) == 1 ]
		degree_units = [ unit for unit in degree_requirements if len(unit.split(" ")) == 1 ]
		remaining_requirements = list(set(degree_requirements).union(set(major_requirements)) - set(major_units).union(set(degree_units)) )
		#print 'remaining_requirements: ', remaining_requirements
		#print 'major_units: ', major_units
		self.remaining_requirements = remaining_requirements

		all_core_units =list(set(major_units).union(set(degree_units)))
		


		#print 'Available Units'
		final_available_units[self.year] = []
		year = self.year

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

			# Todo: Uncomment the following line
			# final_available_units[self.year].append(temp_dict)
			final_available_units[year].append(temp_dict)
			

			all_core_units = list(set(all_core_units) - set(aggregate_student_units))


			if self.session == "s2":
				# Uncomment the following lines
				#self.year = str(int(self.year) + 1)
				#final_available_units[self.year] = []
				year = str(int(year) + 1)
				final_available_units[year] = []
		
		# Todo Uncomment the following
		#if not final_available_units[self.year]:
		#	final_available_units.pop(self.year, None)

		if not final_available_units[year]:
			final_available_units.pop(year, None)
		
		# satisfy_remaining_requirements(remaining_requirements, final_available_units)
		self.planned_student_units = aggregate_student_units
		self.planned_student_units_json = final_available_units
		return final_available_units

	def get_all_units_prior_to_session(self, student_units_json, year, session):
		"""
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
		final_student_units = []
		print 'student_units_json : ', student_units_json
		if not student_units_json:
			student_units_json = self.planned_student_units_json

		for key in student_units_json.keys():
			if int(key) > int(year):
				continue
			if int(key) < int(year):
				final_student_units += (student_units_json[key][0]["s1"])
				final_student_units += (student_units_json[key][1]["s2"])
			elif int(key) == int(year) and session == "s2":
				final_student_units += (student_units_json[key][0]["s1"])
				

		return final_student_units




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
	dp = Degree_Planner('BCom', '', '2014', 's1')
	handbook = Handbook()
	#final = dp.get_available_units_for_entire_degree()
	#print json.dumps(final, sort_keys=True, indent=4)

	#print "Session: ", year, " ",  session

	#s1_units = dp.get_available_units(['COMP115'])
	#print s1_units
	#remaining_requirements = ['COMP225 or COMP229']
	#final_available_units = {'2011': [{'s1': ['COMP115']}, {'s2': ['COMP125', 'DMTH137', 'ISYS114']}], '2013': [{'s1': ['COMP355']}, {'s2': []}], '2012': [{'s1': ['DMTH237']}, {'s2': ['COMP255', 'ISYS224']}]}
	#print dp.satisfy_remaining_requirements(remaining_requirements, final_available_units)
	


