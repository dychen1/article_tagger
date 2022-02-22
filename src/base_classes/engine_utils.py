#!/usr/local/bin/python3 -u

import logging
import os
import urllib.parse

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class EngineUtilities:
    """Base class using SQLAlchemy engines to initialize a database connection. Contains useful
    functions to transact with the database."""

    def __init__(
        self,
        host: str,
        database: str,
        port: int,
        dialect: str,
        recyle_timer: int,
        pool_size: int,
        max_overflow: int,
    ) -> None:
        self.logger = logging.getLogger("EngineUtilitiesLogs")
        self.host = host
        self.database = database
        self.port = port
        self.dialect = dialect

        try:
            self.username = urllib.parse.quote_plus(os.getenv("MYSQL_USER"))
            password = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD"))
        except AttributeError:
            self.logger.error(f"Credentials not found.")
        try:
            conn_args = {"ssl": {"ssl-mode": "required"}}
            self.engine = create_engine(
                f"{dialect}://{self.username}:{password}@"
                f"{self.host}:{self.port}/{self.database}",
                connect_args=conn_args,
                pool_recycle=recyle_timer,
                pool_size=pool_size,
                max_overflow=max_overflow,
            )
            self.init_session = sessionmaker(bind=self.engine)
            self.logger.info(
                f"Engine and sessionmaker configured for {self.database} on {self.host}!"
            )
        except:
            self.logger.error(
                f"Could not configure engine and sessionmaker for {self.database} " f"on {self.host}!"
            )
            raise

    @contextmanager
    def session_manager(self) -> None:
        """Creates a session from session factory and wraps query in session in database transaction."""
        session = self.init_session()
        try:
            yield session
            session.commit()
        except:
            self.logger.warning("Session failed!", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
        return
