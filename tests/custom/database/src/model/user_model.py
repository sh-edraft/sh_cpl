from cpl_core.database import TableABC

from .city_model import CityModel


class UserModel(TableABC):

    def __init__(self, name: str, city: CityModel, id = 0):
        self.UserId = id
        self.Name = name
        self.CityId = city.CityId if city is not None else 0
        self.City = city

    @staticmethod
    def get_create_string() -> str:
        return str(f"""
            CREATE TABLE IF NOT EXISTS `User` (
                `UserId` INT(30) NOT NULL AUTO_INCREMENT,
                `Name` VARCHAR(64) NOT NULL,
                `CityId` INT(30),
                FOREIGN KEY (`UserId`) REFERENCES City(`CityId`),
                PRIMARY KEY(`UserId`)
            );
        """)

    @property
    def insert_string(self) -> str:
        return str(f"""
            INSERT INTO `User` (
                `Name`
            ) VALUES (
                '{self.Name}'
            );
        """)

    @property
    def udpate_string(self) -> str:
        return str(f"""
            UPDATE `User`
            SET `Name` = '{self.Name}', 
            `CityId` = {self.CityId},
            WHERE `UserId` = {self.UserId};
        """)

    @property
    def delete_string(self) -> str:
        return str(f"""
            DELETE FROM `User`
            WHERE `UserId` = {self.UserId};
        """)
