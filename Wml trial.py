import urllib3, requests, json

# retrieve your wml_service_credentials_username, wml_service_credentials_password, and wml_service_credentials_url from the
# Service credentials associated with your IBM Cloud Watson Machine Learning Service instance

wml_credentials={
"url": wml_service_credentials_url,
"username": wml_service_credentials_username,
"password": wml_service_credentials_password
}

headers = urllib3.util.make_headers(basic_auth='{username}:{password}'.format(username=wml_credentials['username'], password=wml_credentials['password']))
url = '{}/v3/identity/token'.format(wml_credentials['url'])
response = requests.get(url, headers=headers)
mltoken = json.loads(response.text).get('token')

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"fields": ["COLUMN1", "COLUMN2", "COLUMN3"], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}

response_scoring = requests.post('https://ibm-watson-ml.eu-gb.bluemix.net/v3/wml_instances/d09f44ec-4b72-40bc-90be-181b2b472af2/published_models/86d13583-2bbc-48be-8cf9-91ed0a203271/deployments/68a730a8-0784-4800-b623-92210812a615/online', json=payload_scoring, headers=header)
print("Scoring response")
print(json.loads(response_scoring.text))