"""
Contains the core functionality of the database.
"""

import sys
import os
from typing import List, Optional

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db.model import Country, Image
from db.setup import SQLBackend
from db.decorator import handle_session


class DatabaseManager(SQLBackend):
    """
    DatabaseManager is used to interact with the database.
    """

    def __init__(self, connection_string: str):
        super().__init__(connection_string)

    @handle_session
    def get_country(self, session, country_name: str) -> Country:
        """
        Get a country from the database.


        Args:
            session: database session
            country_name: name of the country

        Returns:
            Country: country object
        """
        return session.query(Country).filter(Country.name == country_name).first()

    @handle_session
    def add_bulk_countries(self, session, countries: List[dict]):
        """
        Add multiple countries to the database.

        Args:
            session: database session
            countries: list of countries to add

        Returns:
            None
        """
        session.bulk_insert_mappings(Country, countries)
        session.commit()

    @handle_session
    def update_bulk_countries(self, session, countries: List[dict]):
        """
        Update multiple countries in the database.

        Args:
            session: database session
            countries: list of countries to update

        Returns:
            None
        """
        session.bulk_update_mappings(Country, countries)
        session.commit()

    @handle_session
    def get_countries(
        self,
        session,
        limit: Optional[int],
        sort_by: str,
        order_by: str,
    ) -> List[Country]:
        """
        Get all countries from the database.

        Args:
            session: database session
            limit: number of countries to return
            sort_by: field to sort by
            order_by: order of sorting (asc or desc)

        Returns:
            List[Country]: list of country objects
        """
        query = session.query(Country)

        if order_by == "asc":
            query = query.order_by(getattr(Country, sort_by).asc())
        else:
            query = query.order_by(getattr(Country, sort_by).desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    @handle_session
    def add_image_meta_data(self, session, image: Image) -> int:
        """
        Add image meta data to the database.

        Args:
            session: database session
            image: image object to add

        Returns:
            int: id of the image
        """
        session.add(image)
        session.commit()
        return image.id

    @handle_session
    def get_images_meta_data(self, session, country_name: str) -> List[Image]:
        """
        Get images meta data from the database for a specific country.

        Args:
            session: database session
            country_name: name of the country

        Returns:
            List[Image]: list of image objects
        """
        return session.query(Image).filter_by(country_name=country_name).all()
