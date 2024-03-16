import requests

url = "https://v1.nocodeapi.com/kali_user98/fit/lOEQiXwDNbDJnDxw/aggregatesDatasets?dataTypeName=steps_count"
params = {}
r = requests.get(url = url, params = params)
result = r.json()
steps_count = [entry['value'] for entry in result['steps_count']]

