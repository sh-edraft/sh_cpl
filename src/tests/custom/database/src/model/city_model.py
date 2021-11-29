from cpl_core.database import TableABC


class CityModel(TableABC):

    def __init__(self, name: str, zip_code: str):
        self.CityId = 0
        self.Name = name
        self.ZIP = zip_code
    
    @property
    def create_string(self) -> str:
        return f"""
            CREATE TABLE IF NOT EXISTS `City` (
                `CityId` INT(30) NOT NULL AUTO_INCREMENT,
                `Name` VARCHAR NOT NULL,
                `ZIP` VARCHAR NOT NULL,
            );
        """
    
    @property
    def insert_string(self) -> str:
        return f"""
            INSERT INTO `City` (
                `Name`, `ZIP`
            ) VALUES (
                '{self.Name}',
                '{self.ZIP}'
            );
        """
    
    @property
    def udpate_string(self) -> str:
        return f"""
            UPDATE `City`
            SET `Name` = '{self.Name}', 
            `ZIP` = '{self.ZIP}',
            WHERE `CityId` = {self.Id};
        """
    
    @property
    def delete_string(self) -> str:
        return f"""
            DELETE FROM `City`
            WHERE `CityId` = {self.Id};
        """
