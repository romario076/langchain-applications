import requests
import json

API_KEY_PROXY = "VS0Jm8Lf2jLirLKU6g2WAw"

api_key = 'YOUR_API_KEY'
headers = {'Authorization': 'Bearer ' + API_KEY_PROXY}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {'url':'https://www.linkedin.com/in/roman-melnyk-690689b8/'
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)


with open("linkedinData.json", "w") as twitter_data_file:
    json.dump(response.json(), twitter_data_file, indent=4, sort_keys=True)


with open('linkedinData.json') as fp:
    data = json.load(fp)
gist = requests.get('https://gist.githubusercontent.com/romario076/f829f5b40cb8d02e8aa2d3a2168caa9c/raw/ad199b430dac8646f9b6dc0c280de35e72c86edb/roman-melnyk.json')

data = gist.json()
data = {
    k: v
    for k, v in data.items()
    if v not in ([], "", "", None)
       and k not in ["people_also_viewed", "certifications"]
}
if data.get("groups"):
    for group_dict in data.get("groups"):
        group_dict.pop("profile_pic_url")