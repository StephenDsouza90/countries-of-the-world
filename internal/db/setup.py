"""
Creates the database and the tables.
"""

import time

from pymongo import MongoClient

from internal.db.model import COLLECTIONS, DATABASE_NAME


class NoSQLBackend:
    """
    NoSQLBackend is used to setup the database and the collections.
    """

    def __init__(self, connection_string: str):
        self.client = None
        self.db = None
        self.connection_string = connection_string
        self._setup_session(connection_string)

    def _setup_session(self, connection_string=None):
        """
        Setup the client and session.
        If the client is already setup, then return.

        Args:
            connection_string: connection string to the database

        Returns:
            None
        """

        if self.client:
            return

        self.client = MongoClient(connection_string)

    def bootstrap(self, retry: int = 2):
        """
        Bootstrap creates database and collections.
        Retries connecting to MongoDB until it is available.

        Args:
            retry: number of retries

        Returns:
            None

        Raises:
            Exception: if there is an error in the connection
        """

        # Retry connection logic
        for attempt in range(retry):
            try:
                self.client.admin.command("ping")
                print("Connected to MongoDB!")
                break
            except Exception:
                print(f"Attempt {attempt + 1} failed. Retrying in {5} seconds...")
                time.sleep(attempt * 5)
        else:
            raise Exception("Couldn't connect to MongoDB after retries!")

        # Access a database (it will be created if it doesn't exist)
        self.db = self.client[DATABASE_NAME]

        # Access a collection (it will be created if it doesn't exist)
        for collection in COLLECTIONS:
            if collection not in self.db.list_collection_names():
                self.db.create_collection(collection, capped=True, size=5242880)
                print(f"Created collection: {collection}")
            else:
                print(f"Collection already exists: {collection}")
