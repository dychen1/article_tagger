import requests
import json
from pprint import pprint as pp

# SAMPLE POST REQUEST TO SEARCH FOR ARTICLES GIVEN SEARCH CRITERIA

url = "http://127.0.0.1:5000/api/search_articles"

payload = json.dumps({
  "article_id": [],
  "headline": [],
  "published_time": [],
  "publisher_timezone": [],
  "tag": [],
  "tagged_by": [],
  "entities": {
    "city": [
      "montreal"
    ],
    "topic": [
      "comedy"
    ]
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

pp(response.text)
pp(response.status_code)
