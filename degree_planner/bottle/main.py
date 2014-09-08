#!/usr/bin/env python

import sys
import json
import BaseHTTPServer
sys.path.append('/Users/surendrashrestha/Projects/degree_planner/degree_planner')

from degree_parser import *
from handbook import *
from degree_planner import *
from bottle import template, request, redirect, route, post, run, static_file, view

dp = Degree_Planner('BIT', 'SOT01', '2011', 's1')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# Procedure to handle the home page /
@route("/", method='GET')
@route("/", method='POST')
def index(): 
    
    handbook = Handbook()
    pp = Prereq_Parser()
    #degree_planner = Degree_Planner()
    year = '2011'
    


    all_degrees = handbook.extract_all_degrees('2011')
    
    if request.forms:
        degree_code = request.forms.get("degree")
        major_code = request.forms.get("major")
        global dp

        dp = Degree_Planner(degree_code, major_code, '2011', 's1')
        all_available_units = dp.get_available_units_for_entire_degree()
        sorted_years = sorted(all_available_units.keys())

        dp.gen_degree_req = handbook.extract_general_requirements_of_degree(degree_code, '2014')
        dp.degree_req_units = handbook.extract_degree_requirements(degree_code, year)
        dp.major_req_units = handbook.extract_major_requirements(major_code, year)

        
        planned_student_units = list(set(dp.planned_student_units))
        if "True " in planned_student_units:
            planned_student_units.remove("True ")
        
        dp.planned_student_units = planned_student_units

        updated_gen_degree_req = pp.update_general_requirements_of_degree(dp.planned_student_units, dp.gen_degree_req)
        updated_degree_req_units = pp.update_degree_req_units(dp.planned_student_units, dp.degree_req_units)
        updated_major_req_units = pp.update_major_reqs(dp.planned_student_units, dp.major_req_units)

        
        #print updated_gen_degree_req
    else:
        degree_code = major_code = all_available_units = sorted_years = gen_degree_req = degree_req_units = major_req_units = None
        updated_gen_degree_req = updated_degree_req_units = updated_major_req_units = None

    
    return template('index', 
                    all_degrees=all_degrees, 
                    selected_degree=degree_code,
                    selected_major=major_code,
                    all_available_units=all_available_units,
                    sorted_years=sorted_years,
                    gen_degree_req=dp.gen_degree_req,
                    degree_req_units=dp.degree_req_units,
                    major_req_units=dp.major_req_units,
                    updated_gen_degree_req =updated_gen_degree_req,
                    updated_degree_req_units=updated_degree_req_units,
                    updated_major_req_units=updated_major_req_units

                    )


@route("/populate_modal", method='POST')
def index():
    handbook = Handbook()
    print 'request_json: ', request.json
    year_session = str(request.json['year_session'])
    print "year_session:", year_session
    [year, session] = year_session.split('_')

    people_units = dp.people_units
    planet_units = dp.planet_units
    comp_units = dp.comp_units
    filtered_comp_units = handbook.filter_units_by_offering(comp_units, year, session)
    
    # Get all the units prior to that particular session

    student_units = dp.get_all_units_prior_to_session(dp.planned_student_units_json, year, session)
    
    if session == 's1':
        student_units_in_same_session = dp.planned_student_units_json[year][0]['s1']
    else:
        student_units_in_same_session = dp.planned_student_units_json[year][1]['s2']

    print 'student_units_in_same_session: ', student_units_in_same_session
    remaining_comp_units = list(set(filtered_comp_units) - set(student_units) - set(student_units_in_same_session))
    print 'student_units prior to session: ', student_units

    # Todo
    # Find the prereq and get all the units which satisfy the prereq
    available_comp_units = dp.filter_units_by_prereq(student_units, remaining_comp_units, year)
    print 'available comp units: ', available_comp_units




    #filtered_people_units = handbook.filter_units_by_offering(people_units, year, session)
    #filtered_planet_units = handbook.filter_units_by_offering(planet_units, year, session)
    

    #return {"planet_units": filtered_planet_units, "people_units": filtered_people_units}
    return {    "planet_units": planet_units, 
                "people_units": people_units,
                "comp_units": available_comp_units
            }


@route("/populate_major", method='POST')
def index():
    handbook = Handbook()
    degree_code = str(request.json['degree_code'])
    majors = handbook.extract_all_majors_of_degree(degree_code, '2014')
    return {"majors": majors}



@route("/update_requirements", method='POST')
def index():
    global dp
    pp = Prereq_Parser()

    selected_unit = str(request.json['selected_unit']).strip()
    dp.planned_student_units.append(selected_unit)
    
    # Update planned_student_units_json
    year_session = str(request.json['year_session'])
    [year, session] = year_session.split('_')
    if session == 's1':
        dp.planned_student_units_json[year][0]['s1'].append(selected_unit)
    elif session == 's2':
        dp.planned_student_units_json[year][1]['s1'].append(selected_unit)

    updated_gen_degree_req = pp.update_general_requirements_of_degree(dp.planned_student_units, dp.gen_degree_req)
    updated_degree_req_units = pp.update_degree_req_units(dp.planned_student_units, dp.degree_req_units)
    updated_major_req_units = pp.update_major_reqs(dp.planned_student_units, dp.major_req_units)

    return {"updated_gen_degree_req" : updated_gen_degree_req,
            "updated_degree_req_units" :updated_degree_req_units,
            "updated_major_req_units" : updated_major_req_units
            }

if __name__ == "__main__":
    # start a server but have it reload any files that
    # are changed
    setattr(BaseHTTPServer.HTTPServer,'allow_reuse_address',0)
    run(host="localhost", port=8000, reloader=True)

