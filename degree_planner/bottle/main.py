#!/usr/bin/env python

import sys
import json
sys.path.append('/Users/surendrashrestha/Projects/degree_planner/degree_planner')

from degree_parser import *
from handbook import *
from degree_planner import *
from bottle import template, request, redirect, route, post, run, static_file


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


@route("/populate_major", method='POST')
def index():
    handbook = Handbook()
    degree_code = str(request.json['degree_code'])
    majors = handbook.extract_all_majors_of_degree(degree_code, '2014')
    return {"majors": majors}




@route("/wordcloud")
def index():
    
    client = hcsvlab.Client()
    
    wordfrequency = word_frequency.get_word_frequency_table(client)
    
    words = [word[0] for word in wordfrequency]
    word_dict = dict(wordfrequency)
    words =json.dumps(words)
    word_dict = json.dumps(word_dict)
    #words = ""
    
    #print words
    
    return template('wordcloud', 
                    words=words, 
                    word_dict=word_dict, 
                    shared_item_list = get_shared_item_lists(client),
                    personal_item_list = get_personal_item_lists(client)

                    )

@route("/heatmap", method="GET")
@route("/heatmap", method="POST")
def index():
    client = hcsvlab.Client()
    
    words = request.forms.getall("words[]")
    item_list_name = request.forms.get("item_list_name")

    if words and item_list_name:
        [row_words, col_words] = word_frequency.get_collocation_frequency(client, item_list_name, words)
    else:
        [row_words, col_words] = word_frequency.get_collocation_frequency(client, item_list_name)

    row_words= json.dumps(row_words)
    col_words = json.dumps(col_words)
    print row_words

    return template('heatmap', 
                    row_words = row_words, 
                    col_words = col_words, 
                    personal_item_list = get_personal_item_lists(client)

                    )


@route("/visualise", method='POST')
def index():
    client = hcsvlab.Client()
    item_list_name = str(request.json['item_list_name'])
    
    wordfrequency = word_frequency.get_word_frequency_table(client, item_list_name)
    #wordfrequency = wordfrequency[0:10]
    words = [word[0] for word in wordfrequency]
    word_dict = dict(wordfrequency)
    words =json.dumps(words)
    word_dict = json.dumps(word_dict)
    
    #print item_list_name
    #return { "list" : item_list_name}
    return {"words": words, "word_dict": word_dict}

@route("/timeline", method="POST")
@route("/timeline", method="GET")
def index():
    

    words = request.forms.getall("words[]")
    pos = request.forms.getall("pos[]")
    
    print words
    print pos

    item_list_name = request.forms.get("item_list_name")

    word_list = []
    file = open("./static/timeline.tsv", "w")
    file.write("date")
    i=0
    

    for word in words:
        file.write("\t" + word + '_' + pos[i])    
        result = word_frequency.get_word_frequency_per_year(client, word, pos[i], item_list_name)
        if result:
            word_list.append(result)
        i = i + 1
    
    #an_list = word_frequency.get_word_frequency_per_year(client,'an', 'cooee list')
    #a_list = word_frequency.get_word_frequency_per_year(client,'a', 'cooee list')
    file.write("\n")

    if not word_list:
        return template('timeline', rows=[], personal_item_list = get_personal_item_lists(client))


    print word_list
   
    for key in sorted(word_list[0]):
        file.write(key);
        for i in range(len(word_list)):
            file.write("\t" + str(word_list[i][key]))
        file.write("\n")

    file.close()

    file = open("./static/timeline.tsv", "r")
    content = file.read()

    rows = content.split("\n")[:-1]
    

    file.close()
    
    print words
    return template('timeline', rows=rows, personal_item_list = get_personal_item_lists(client))

if __name__ == "__main__":
    # start a server but have it reload any files that
    # are changed
    run(host="localhost", port=8000, reloader=True)

