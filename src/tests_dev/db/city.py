from sqlalchemy import Column, Integer, String

from sh_edraft.database.model import DBModel


class City(DBModel):
    __tablename__ = 'Cities'
    Id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Name = Column(String(64), nullable=False)
    ZIP = Column(String(5), nullable=False)

    def __init__(self, name: str, zip_code: str):
        self.Name = name
        self.ZIP = zip_code
