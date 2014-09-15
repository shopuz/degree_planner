from setuptools import setup, find_packages

def readme():
	with open('README.md') as f:
		return f.read()


setup(	name='degree_planner',
		version='0.1',
		description="A tool to plan and check degree for university students",
		long_description=readme(),
		url='https://github.com/shopuz/degree_planner',
		maintainer='',
		maintainer_email='',
		license='BSD',
		keywords='degree planner, degree checker, degree navigator',
		packages = find_packages(exclude=['contrib', 'docs', 'tests*']),

		install_requires=[
			'pyparsing',
			'bottle',
			'beaker'
		],
		test_suite='nose.collector',
    	tests_require=['nose'],
		include_package_data=True,
		zip_safe=False)