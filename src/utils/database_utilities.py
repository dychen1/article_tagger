#!/usr/local/bin/python3 -u

from collections import OrderedDict
import logging
from typing import Any, Dict, List

from base_classes.engine_utils import EngineUtilities
from models.db_models import Article, Entity, Tag


class DatabaseUtilities(EngineUtilities):
    """Utilities class inheriting from EngineUtilities to perform queries on the database."""

    def __init__(
        self,
        host: str,
        database: str,
        port: int = 3306,
        dialect: str = "mysql+pymysql",
        recyle_timer: int = 14400,
        pool_size: int = 5,
        max_overflow: int = 5,
    ) -> None:
        super().__init__(host, database, port, dialect, recyle_timer, pool_size, max_overflow)
        self.logger = logging.getLogger("DatabaseUtilitiesLogs")

    def query_all_articles(self) -> List[Any]:
        """Queries all articles and returns them by latest published time."""
        with self.session_manager() as session:
            articles = (
                session.query(Article.article_id, Article.headline, Article.published_time)
                .order_by(Article.published_time.desc())
                .all()
            )
        return articles

    def query_by_article(self, searched: Dict[str, Any]) -> List[str]:
        """Query articles table for articles corresponding to given search attributes.
        Returns a list of article ids."""
        with self.session_manager() as session:
            articles_query = session.query(Article.article_id)

            article_ids = searched.get("article_id")
            if article_ids:
                articles_query = articles_query.filter(Article.article_id.in_(article_ids))

            headlines = searched.get("headline")
            if headlines:
                articles_query = articles_query.filter(Article.headline.in_(headlines))
            # Execute query
            articles = articles_query.all()
        return [article.article_id for article in articles]

    def query_by_tags(self, tags: List[str]) -> List[str]:
        """Query tags table articles corresponding to searched tags.
        Returns a list of article ids."""
        with self.session_manager() as session:
            articles = session.query(Tag.article_id).filter(Tag.tag.in_(tags)).all()
        return [article.article_id for article in articles]

    def query_by_entities(self, entities: Dict[str, List[str]]) -> List[str]:
        """Query entities table for articles corresponding to given search attributes.
        Returns a list of article ids."""
        article_ids = []
        with self.session_manager() as session:
            # Cascading search to narrow down articles ids which satisfy all search parameters
            for entity, entity_values in entities.items():
                articles = (
                    session.query(Entity.article_id)
                    .filter(Entity.entity == entity)
                    .filter(Entity.entity_value.in_(entity_values))
                    .all()
                )
                current_article_ids = [article.article_id for article in articles]
                if not current_article_ids:
                    # No articles found with current entity and entity values set
                    return []
                elif not article_ids:
                    article_ids.extend(current_article_ids)
                else:
                    # Take articles which satisfy searched criteria
                    article_ids = list(set(article_ids) & set(current_article_ids))
                    if not article_ids:
                        return []
        return article_ids

    def query_article_by_article_id(self, article_ids: List[str], desc: bool) -> Dict[str, Dict[str, str]]:
        """Queries by article ids on article table. Creates base articles_dict to attach article attributes to.
        Returns a dictionary mapping article id to an article dict containing article attributes and values."""
        with self.session_manager() as session:
            articles = (
                session.query(
                    Article.article_id,
                    Article.headline,
                    Article.published_time,
                    Article.publisher_timezone,
                    Article.article_content,
                )
                .filter(Article.article_id.in_(article_ids))
            )
            if desc:
                articles = articles.order_by(Article.published_time.desc())
            else:
                articles = articles.order_by(Article.published_time.asc())
            articles.all()

        # Dictionary of article ids mapped to article dict object
        # i.e. { article_id: { article_id: abc123, headline: headline1, ... } }
        articles_dict = OrderedDict()
        for article in articles:
            articles_dict[article.article_id] = article._asdict()
        self.logger.debug("articles_dict: ", articles_dict)
        return articles_dict

    def query_entities_by_article_id(self, article_ids: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """Queries by article ids on entities table. Pulls all entities belonging to articles corresponding to
        search criteria. Maps entities and entity values to their associated article id in a dict.
        Returns a dictionary mapping article id to a dict of entities mapped to a list of their values."""
        with self.session_manager() as session:
            entities = (
                session.query(
                    Entity.article_id,
                    Entity.entity,
                    Entity.entity_value
                    )
                .filter(Entity.article_id.in_(article_ids))
                .all()
            )
        # Dictionary of article ids mapped to entities mapped to entity values
        # i.e. { article_id: { entity1: [entity_values], entity2: [entity_values, ...] } }
        entities_dict = {}
        for entity in entities:
            article_entities = entities_dict.get(entity.article_id)
            if article_entities:
                if entity.entity in article_entities:
                    article_entities[entity.entity].append(entity.entity_value)
                else:
                    article_entities[entity.entity] = [entity.entity_value]
            else:
                entities_dict = {entity.article_id: {entity.entity: [entity.entity_value]}}
        self.logger.debug("entities_dict: ", entities_dict)
        return entities_dict

    def query_tag_by_article_id(self, article_ids: List[str]) -> Dict[str, List[str]]:
        """Queries by article id on tags table. Pulls all tags associated with an article.
        Returns a dictionary mapping an article id with a list of its tags."""
        with self.session_manager() as session:
            tags = (
                session.query(
                    Tag.article_id,
                    Tag.tag
                    )
                .filter(Tag.article_id.in_(article_ids))
                .all()
            )
            # Dictionary of article ids mapped to tag dicts mapped to the tag value
            # i.e. { article_id: [tag1, tag2, ...] }
            tags_dict = {}
            for tag in tags:
                article_tags = tags_dict.get(tag.article_id)
                if article_tags:
                    article_tags.append(tag.tag)
                else:
                    tags_dict = {tag.article_id: [tag.tag]}
        self.logger.debug("tags_dict: ", tags_dict)
        return tags_dict

    def insert_tags(self, tags: List[Dict[str, str]]) -> None:
        """Bulk inserts list of tags for given article id."""
        with self.session_manager() as session:
            session.bulk_insert_mappings(Tag, tags)
        return
