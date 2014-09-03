#!/usr/bin/env python

import sys
import json
sys.path.append('/Users/surendrashrestha/Projects/degree_planner/degree_planner')

from degree_parser import *
from handbook import *
from degree_planner import *
from bottle import template, request, redirect, route, post, run, static_file

dp = Degree_Planner('BIT', 'SOT01', '2011', 's1')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

def get_shared_item_lists(client):
    
    lists = client.get_item_lists()
    return lists['shared']

def get_personal_item_lists(client):
    
    lists = client.get_item_lists()
    return lists['own']

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

        dp = Degree_Planner(degree_code, major_code, '2011', 's1')
        all_available_units = dp.get_available_units_for_entire_degree()
        sorted_years = sorted(all_available_units.keys())

        gen_degree_req = handbook.extract_general_requirements_of_degree(degree_code, '2014')
        degree_req_units = handbook.extract_degree_requirements(degree_code, year)
        major_req_units = handbook.extract_major_requirements(major_code, year)

        planned_student_units = list(set(dp.aggregate_student_units))
        if "True " in planned_student_units:
            planned_student_units.remove("True ")

        print 'planned_student_units: ', planned_student_units
        print 'general_degree_req: ', gen_degree_req

        updated_gen_degree_req = pp.update_general_requirements_of_degree(planned_student_units, gen_degree_req)
        updated_degree_req_units = pp.update_degree_req_units(planned_student_units, degree_req_units)
        updated_major_req_units = pp.update_major_reqs(planned_student_units, major_req_units)

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
                    gen_degree_req=gen_degree_req,
                    degree_req_units=degree_req_units,
                    major_req_units=major_req_units,
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
    
    filtered_people_units = handbook.filter_units_by_offering(people_units, year, session)
    filtered_planet_units = handbook.filter_units_by_offering(planet_units, year, session)

    return {"planet_units": filtered_planet_units, "people_units": filtered_people_units}


@route("/populate_major", method='POST')
def index():
    handbook = Handbook()
    degree_code = str(request.json['degree_code'])
    majors = handbook.extract_all_majors_of_degree(degree_code, '2014')
    return {"majors": majors}



if __name__ == "__main__":
    # start a server but have it reload any files that
    # are changed
    
    run(host="localhost", port=8000, reloader=True)

