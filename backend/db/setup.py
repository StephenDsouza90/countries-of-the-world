"""
Creates the database and the tables.
"""

import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.model import Base


class SQLBackend:
    """
    SQLBackend is used to setup the database and the tables.
    """

    def __init__(self, connection_string: str):
        self.engine = None
        self.Session = sessionmaker(autocommit=False, expire_on_commit=False)
        self._setup_session(connection_string)

    def _setup_session(self, connection_string=None):
        """
        Setup the engine and session.
        If the engine is already setup, then return.

        Args:
            connection_string: connection string to the database

        Returns:
            None
        """

        if self.engine:
            return

        self.engine = create_engine(connection_string)
        self.Session.configure(bind=self.engine)

    def bootstrap(self, retry: int = 2):
        """
        Bootstrap creates database and tables.
        Assumes no databases have been setup.
        Retries until connection is established.

        Args:
            retry: number of retries to connect to the database

        Returns:
            None

        Raises:
            Exception: if there is an error in the connection
        """

        connection = None

        for i in range(retry):
            try:
                connection = self.engine.connect()
            except Exception:
                print("DB is probably not up yet, Retrying ...")
                time.sleep(i * 5)
                continue

        if not connection:
            raise Exception("Couldn't connect to DB even after retries!")

        Base.metadata.create_all(self.engine)
        connection.close()
