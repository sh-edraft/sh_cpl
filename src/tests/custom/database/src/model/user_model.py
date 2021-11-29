from cpl_core.database import TableABC

from .city_model import CityModel


class UserModel(TableABC):

    def __init__(self, name: str, city: CityModel):
        self.UserId = 0
        self.Name = name
        self.CityId = city.CityId
        self.City = city

    @property
    def create_string(self) -> str:
        return f"""
            CREATE TABLE IF NOT EXISTS `User` (
                `UserId` INT(30) NOT NULL AUTO_INCREMENT,
                `Name` VARCHAR NOT NULL,
                `CityId` VARCHAR NOT NULL,
                FOREIGN KEY (`UserId`) REFERENCES City(`CityId`),
                PRIMARY KEY(`UserId`)
            );
        """

    @property
    def insert_string(self) -> str:
        return f"""
            INSERT INTO `User` (
                `Name`
            ) VALUES (
                '{self.Name}'
            );
        """

    @property
    def udpate_string(self) -> str:
        return f"""
            UPDATE `User`
            SET `Name` = '{self.Name}', 
            `CityId` = {self.CityId},
            WHERE `UserId` = {self.UserId};
        """

    @property
    def delete_string(self) -> str:
        return f"""
            DELETE FROM `User`
            WHERE `UserId` = {self.UserId};
        """
