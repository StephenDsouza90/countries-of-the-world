"""
Country object that will be mapped to the country table.
"""

import warnings
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
# Official Docks: https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html

# Suppress the MovedIn20Warning for declarative_base
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r"The ``declarative_base\(\)`` function is now available as sqlalchemy.orm.declarative_base\(\)\.",
)

# NOTE: According to the official SQLAlchemy docs,
# the declarative_base should be imported from sqlalchemy.ext.declarative
# However, when running the tests, a warning is raised
# MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base().
# (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
#    Base = declarative_base()
# -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
# Hence, suppressing the warning


Base = declarative_base()


class Country(Base):
    """
    This class is used to create the country table.
    """

    __tablename__ = "countries"

    name = Column(String, primary_key=True, nullable=False)
    region = Column(String, nullable=False)
    population = Column(Integer, nullable=False)
    area = Column(Float, nullable=False)
    population_density = Column(Float, nullable=False)

    def to_dict(self):
        """
        Convert the country object to a dictionary.
        :return: dict: country object as a dictionary
        """
        return {
            "name": self.name,
            "region": self.region,
            "population": self.population,
            "area": self.area,
            "population_density": self.population_density,
        }


class Image(Base):
    """
    This class is used to create the image table that stores image meta data.
    """

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, nullable=False)
    country_name = Column(String, ForeignKey("countries.name"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
