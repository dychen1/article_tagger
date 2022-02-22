import requests
from pprint import pprint as pp

# SAMPLE GET REQUEST TO RETURN ALL ARTICLES ORDERED BY PUBLISHED TIME DESC

url = "http://127.0.0.1:5000/api/get_all_articles"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

pp(response.text)
pp(response.status_code)