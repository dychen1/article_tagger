from flask import Flask, request
import logging
import os
from typing import Any, Dict, Tuple
import traceback

from utils.database_utilities import DatabaseUtilities
from utils.init_logger import init_logger
from utils.request_parser import parse_tag_article, parse_searched, is_desc


app = Flask(__name__)
db_utils = DatabaseUtilities(
    host=os.getenv("DATABASE_CONTAINER"), database=os.getenv("MYSQL_DATABASE")
)

init_logger()
logger = logging.getLogger("ArticleTaggerLogs")


@app.route("/", methods=["GET"])
def home():
    return "Article tagger API home"


@app.route("/api/get_all_articles", methods=["GET"])
def get_all_articles() -> Tuple[Dict[str, Any], int]:
    """Returns all articles, headlines and publishing time ordered by latest publishing time."""
    response = {}
    try:
        articles = db_utils.query_all_articles()
        # List of row objects to list of dicts
        response["content"] = [article._asdict() for article in articles]
        msg = "All articles returned"
        status = 200
    except:
        msg = "Unable to fetch articles! Here is the traceback:\n" + traceback.format_exc()
        status = 500
    response["message"] = msg
    logger.debug("Get all articles msg:", msg)
    return (response, status)


@app.route("/api/search_articles", methods=["GET"])
def search_articles() -> Tuple[Dict[str, Any], int]:
    """Returns articles by search criteria in GET request. Currently only supports
    exact string matching.

    Body format for GET request should be a JSON object (dictionary) where keys represent
    article attributes.
    Ex:
    {
        "article_id": [],
        "headline": [],
        "published_time": [],
        "publisher_timezone": [],
        "tag": ["news"],
        "entity": {
            "city": ["toronto"],
            "topic": ["covid-19"]
        },
        "order_by_time": "desc"
    }
    """
    response = {}
    searched = request.json
    article_ids = parse_searched(db_utils, searched)
    try:
        articles_dict = db_utils.query_article_by_article_id(article_ids, desc=is_desc(searched))
        entities_dict = db_utils.query_entities_by_article_id(article_ids)
        tags_dict = db_utils.query_tag_by_article_id(article_ids)
        if entities_dict:
            # Attach entities to its article in articles_dict
            for article_id, entity_dict in entities_dict.items():
                articles_dict[article_id].update({"entity": {}})
                articles_dict[article_id]["entity"].update(entity_dict)
        if tags_dict:
            # Attach tags to its article in articles_dict
            for article_id, tag_dict in tags_dict.items():
                articles_dict[article_id].update({"tags": tag_dict})

        response["content"] = articles_dict
        msg = "Search results returned"
        status = 200
    except:
        msg = "Unable to perform search! Here is the traceback:\n" + traceback.format_exc()
        status = 500
    response["message"] = msg
    logger.debug("Search articles msg:", msg)
    return (response, status)


@app.route("/api/tag_article", methods=["POST"])
def tag_article() -> Tuple[Dict[str, Any], int]:
    """Adds tags to an article given the article id. List of tag values should be mapped
    to the tag. Article id must already exist in articles table.

    Format for body of POST request should be a JSON object (list of dictionaries). Dictionary
    must contain "article_id" key and "tags" key.
    "article_id" - Maps to the string value of the article user would like to tag.
    "tags" - Maps to a list of string tags.
    Ex:
    [
        {"article_id": "abc123", "tags": ["news", "global"]},
        {"article_id": "abc456", "tags": ["travel"]}
    ]
    """
    response = {}
    tagged_articles = request.json
    tags_to_insert = parse_tag_article(tagged_articles, db_utils.username)
    try:
        db_utils.insert_tags(tags_to_insert)
        status = 200
        msg = "Tagging successful!"
        response["inserted_tags"] = tags_to_insert
    except:
        status = 500
        msg = "Tagging unsuccessful! Here is the traceback:\n" + traceback.format_exc()
    response["message"] = msg
    logger.debug("Tag articles msg:", msg)
    return (response, status)
