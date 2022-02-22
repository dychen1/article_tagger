import requests
import json
from pprint import pprint as pp

# SAMPLE POST REQUEST TO TAG ARTICLES

url = "http://127.0.0.1:5000/api/tag_article"

payload = json.dumps([
  {
    "article_id": "abc123",
    "tags": [
      "news",
      "global"
    ]
  },
  {
    "article_id": "abc456",
    "tags": [
      "travel"
    ]
  }
])
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pp(response.text)
pp(response.status_code)
