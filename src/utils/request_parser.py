from typing import Any, Dict, List, Union

from utils.database_utilities import DatabaseUtilities


def is_desc(searched: Dict[str, Any]) -> bool:
    """Takes JSON request and determines if reseponse items are to be ordered
    in descending published_time or ascending published_time.
    Returns a boolean."""
    desc = True
    order_by_time = searched.get("order_by_time")
    if order_by_time:
        if order_by_time == "asc":
            desc = False
    return desc


def parse_searched(db_utils: DatabaseUtilities, searched: Dict[str, Any]) -> List[str]:
    """Parse JSON request to determine the article id(s) which satisfy all search criteria
    provided. Does this by querying each table with their respective search criteria and
    determines the intersection/common article ids."""
    article_ids = []
    # Search by article
    if searched.get("article_id") or searched.get("headline"):
        article_searched_ids = db_utils.query_by_article(searched)
        if not article_searched_ids:
            return []
        else:
            article_ids.extend(article_searched_ids)

    # Search by tag
    if searched.get("tag"):
        tag_searched_ids = db_utils.query_by_tags(searched.get("tag"))
        if not tag_searched_ids:
            return []
        elif article_ids:
            # Get intersection
            article_ids = list(set(article_ids) & set(tag_searched_ids))
            if not article_ids:
                # No common articles between search criteria
                return []
        else:
            article_ids.extend(tag_searched_ids)

    # Search by entity
    if searched.get("entity"):
        entity_searched_ids = db_utils.query_by_entities(searched.get("entity"))
        if not entity_searched_ids:
            return []
        elif article_ids:
            # Get intersection
            article_ids = list(set(article_ids) & set(tag_searched_ids))
            if not article_ids:
                # No common articles between search criteria
                return []
        else:
            article_ids.extend(entity_searched_ids)
    return article_ids


def parse_tag_article(
    tagged_articles: List[Dict[str, Union[str, List[str]]]],
    username: str
) -> List[Dict[str, str]]:
    """Parse JSON request to determine article ids to be tagged and their tags."""
    tags_to_insert = []
    for tagged_article in tagged_articles:
        # List comprehension to flatten JSON request to a list of dictionaries
        flattened_tagged_article = [
            {
                "article_id": tagged_article["article_id"],
                "tag": tag,
                "tagged_by": username,
            }
            for tag in tagged_article["tags"]
        ]
        tags_to_insert.extend(flattened_tagged_article)
    return tags_to_insert
