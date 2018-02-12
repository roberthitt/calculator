import os
import sys

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Image(Base):
    """
    SQLAlchemy class for Image table.
    Contains the columns timestamp, path, and equation.
    """
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    path = Column(String(200), nullable=False)
    equation = Column(String(50), nullable=False)


class StorageEngine:
    """
    Class for interacting with SQLite database.
    """

    def __init__(self):
        self.engine = create_engine('sqlite:///store.db')

        Base.metadata.create_all(self.engine)

    def add_image(self, timestamp, path, equation):
        """
        Write a new image info row to the SQLite DB.

        Args:
            timestamp: time that the graph was created
            path: name that the graph is saved under
            equation: a string containing the right side of an equation
        """

        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        new_image = Image(timestamp=timestamp, path=path, equation=equation)
        session.add(new_image)
        session.commit()

