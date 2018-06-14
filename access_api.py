import requests
import json


#json_content = {
#"set_of_strings" : [{"value": "commute"},
#                  {"value": "communicate"},
#                  {"value": "commutation"}]
#}

json_content = {
"set_of_strings" : [{"value": "fourbroadcaster"},
                    {"value": "fourcraigcaster"},
                    {"value": "fourchcaster"},
                    {"value": "fourchromcasteric"},
                    {"value": "zzzz"}
                  #  {"value": "four"}
                    
                ]
}



print "json_content: " + str(json_content)

# encode
json_content = json.dumps(json_content)

print "serialized json: " + str(json_content)

payload = {"json_data": json_content}
url = "http://localhost:5000/largest_string_match"

res = requests.post(url, headers={'Content-type': 'application/json'},data=json.dumps(payload))
print res.text
print res.status_code
print res.headers['content-type']
