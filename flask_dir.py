from flask import Flask
from flask import request
from difflib import SequenceMatcher
import re
import json
import requests
import httplib

application = Flask(__name__)

@application.route("/largest_string_match", methods=['POST', 'GET'])
def message_factory():
    (joined_list, joined_string) = translate_json(request.get_json(force=True))
    retval = find_largest_strings(joined_list, joined_string)

    status_code = 200
    if not retval:
        status_code = 400

    retval = json.dumps({"lcs" : [{"value": retval}]})
        
    res_obj = application.response_class(
        response=retval,
        status=status_code,
        mimetype='application/json'
    )
    
    return res_obj
    
    
def translate_json(json_data):
    """translates the json into an appropriate datastructure"""

    print "json_data type is: " + str(type(json_data))

    dicts_of_words = json_data['json_data']
    print "json str: " + str(request.json['json_data'])
    data_dict = json.loads(request.json['json_data'])
    print "data_dict type: " + str(type(data_dict))
    print "set_of_strings: " + str(data_dict["set_of_strings"])
    list_of_dicts = data_dict["set_of_strings"]

    joined_list = []

    for each_dict in list_of_dicts:
        print "value: " + str(each_dict['value'])
        joined_list.append(each_dict['value'])

    joined_list.sort(key=len, reverse=True)    
    joined_string = "-".join(joined_list)

    print "joined_string: " + str(joined_string)
    print "joined_list: " + str(joined_list)

    return (joined_list, joined_string)


def find_largest_strings(list_of_strings, joined_string):
    """takes a list and a concatenated list to find teh largest common string"""

    matched_string = None
    retval = None
    list_of_matches = []

    while len(list_of_strings) >= 2: 

        match = SequenceMatcher(None, list_of_strings[0], list_of_strings[1]).find_longest_match(0, len(list_of_strings[0]), 0, len(list_of_strings[1]))
        
        print match
        print list_of_strings[0][match.a: match.a + match.size] 
        print list_of_strings[1][match.b: match.b + match.size]

        matched_string = list_of_strings[0][match.a: match.a + match.size]
        if matched_string:
            list_of_matches.append(matched_string)
        else:
            list_of_matches.append(None)
        
        p1 = re.compile(list_of_strings[0])
        p2 = re.compile(list_of_strings[1])
        if not matched_string and not p1.findall("-") and not p2.findall("-"):
            retval = None
            break

        # adding matched string back to the hyphenated list of strings
        if matched_string:
            print "matched_string: " + str(matched_string)
            joined_list = joined_string.split("-")
            single_string = joined_list.pop(len(joined_list)-1)
            joined_string = "-".join(joined_list)

            p1 = re.compile(matched_string)
            
            list_to_compare = joined_list
            list_to_compare.append(single_string)
            list_to_compare.append(matched_string)
            print "list_to_compare: " + str(list_to_compare)
            ret_list = filter (lambda x: p1.findall(x),list_to_compare)
            ret_list2 = filter (lambda x: matched_string == x, list_to_compare)
            
            print "ret_list: " + str(ret_list)
            print "list_to_compare: " + str(list_to_compare)
            print "ret_list2: " + str(ret_list2)
            # remove duplicates
            list_to_compare = list(set(list_to_compare))

            # if there is one elem we have found the lcm
            if len(list_to_compare) == 1:
                break
            
            # the lcm is an exact match among the strings    
            if len(ret_list) == len(list_to_compare) and len(ret_list2) == 1:
                break

            #if len(ret_list) == len(list_to_compare) and not len(ret_list2) == 1:
            if len(ret_list) and not len(ret_list2) == 1:
                # adding matched string to the front of thelist
                print "adding matched_string"
                joined_string = matched_string + "-" + joined_string
 
            list_of_strings = [joined_string, single_string]
            print "new joined_string: " + str(joined_string)
            print "new list_of_strings: " + str(list_of_strings)
        else:
            try:
                single_string = joined_list.pop(len(joined_list)-1)
                joined_string = "-".join(joined_list)
                list_of_strings = [joined_string, single_string]
                retval = list_of_matches[len(list_of_matches)-1]
                print "no matching string this iteration...found match previous interation"
                break
            except IndexError as e:
                print "Encountered an IndexError: "+ str(e)

            print "new joined_string:" + str(joined_string)
            print "new list_of_strings: " + str(list_of_strings)

    print "list_of_strings: " + str(list_of_strings)
    print "list of matched: " + str(list_of_matches)
    try:
        list_of_matches[len(list_of_matches)-1]
    except IndexError as e:
        return None
    else:
        return list_of_matches[len(list_of_matches)-1]


if (__name__ == "__main__"):
   application.run(host='0.0.0.0')


