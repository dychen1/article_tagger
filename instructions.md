# Article attributes:
```
article_id (string)
headline (string)
published_time (datetime)
publisher_timezone (string) (timezone names from database. ex: America/Toronto)
article_content (string)
entities (map<string, list<string>>) (the entities found within the article. An example, entities map would look like below
                                            {
                                            'cities': ['Toronto', 'Montreal'],
                                            'organizations': ['Pfizer', 'RAMQ'],
                                            'topics': ['health', 'vaccine', 'covid-19']
                                            }
                                    )
```

# Functional requirements:
- Tagging the articles which may be of interest to the domain (like business, crime etc) which the journalist is interested in.
- Searching for news articles. The search is a free text search and additional filters as per the tags that the article is tagged with.
- The return list of articles should be in the chronological order (or reverse chronological order) of the published time.

- Following are the non-functional requirements
  - Our service needs to be highly available.
  - Acceptable latency of the system is 1sec for search results.
  - Consistency can take a hit (in the interest of availability); if a user doesn’t see a recent published article for a while, it should be fine.