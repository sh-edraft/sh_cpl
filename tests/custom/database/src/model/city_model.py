from cpl_core.database import TableABC


class CityModel(TableABC):
    def __init__(self, name: str, zip_code: str, id=0):
        self.CityId = id
        self.Name = name
        self.ZIP = zip_code

    @staticmethod
    def get_create_string() -> str:
        return str(
            f"""
            CREATE TABLE IF NOT EXISTS `City` (
                `CityId` INT(30) NOT NULL AUTO_INCREMENT,
                `Name` VARCHAR(64) NOT NULL,
                `ZIP` VARCHAR(5) NOT NULL,
                PRIMARY KEY(`CityId`)
            );
        """
        )

    @property
    def insert_string(self) -> str:
        return str(
            f"""
            INSERT INTO `City` (
                `Name`, `ZIP`
            ) VALUES (
                '{self.Name}',
                '{self.ZIP}'
            );
        """
        )

    @property
    def udpate_string(self) -> str:
        return str(
            f"""
            UPDATE `City`
            SET `Name` = '{self.Name}', 
            `ZIP` = '{self.ZIP}',
            WHERE `CityId` = {self.Id};
        """
        )

    @property
    def delete_string(self) -> str:
        return str(
            f"""
            DELETE FROM `City`
            WHERE `CityId` = {self.Id};
        """
        )
