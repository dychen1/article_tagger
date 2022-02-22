# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Article(Base):
    __tablename__ = 'articles'

    article_id = Column(String(90), primary_key=True)
    headline = Column(String(450), nullable=False)
    published_time = Column(DateTime, nullable=False, index=True)
    publisher_timezone = Column(String(90), nullable=False, index=True)
    article_content = Column(LONGTEXT)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(String(45), nullable=False)


class Entity(Base):
    __tablename__ = 'entities'
    __table_args__ = (
        Index('entity_entity_value_idx', 'entity', 'entity_value'),
    )

    entity_id = Column(INTEGER(11), primary_key=True)
    article_id = Column(ForeignKey('articles.article_id'), nullable=False, index=True)
    entity = Column(String(45), nullable=False)
    entity_value = Column(String(90), nullable=False)
    updated_at = Column(DateTime, nullable=False)
    updated_by = Column(String(45), nullable=False)

    article = relationship('Article')


class Tag(Base):
    __tablename__ = 'tags'
    __table_args__ = (
        Index('tag_tag_value_idx', 'tag', 'tag_value'),
    )

    tag_id = Column(INTEGER(11), primary_key=True)
    article_id = Column(ForeignKey('articles.article_id'), nullable=False, index=True)
    tag = Column(String(45), nullable=False)
    tag_value = Column(String(45), nullable=False)
    tagged_at = Column(DateTime, nullable=False)
    tagged_by = Column(String(45), nullable=False)

    article = relationship('Article')
