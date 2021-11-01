from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from cpl_core.database import DatabaseModel
from .city_model import CityModel


class UserModel(DatabaseModel):
    __tablename__ = 'Users'
    Id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Name = Column(String(64), nullable=False)
    City_Id = Column(Integer, ForeignKey('Cities.Id'), nullable=False)
    City = relationship("CityModel")

    def __init__(self, name: str, city: CityModel):
        self.Name = name
        self.City_Id = city.Id
        self.City = city
