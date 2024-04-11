from uc3m_travel.attribute.attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException
import re

class IdCard(Attribute):
    def __init__(self, attr_value):
        self._regex_pattern = r'^[0-9]{8}[A-Z]{1}$'
        self._error_message = "Invalid IdCard format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, id_card):
        super()._validate(id_card)
        if not self.validate_dni(id_card):
            raise HotelManagementException("Invalid IdCard letter")
        return id_card

    def validate_dni(self, dni ):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        diccionarioLetras = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        numeros = int(dni[ 0:8 ])
        resto = str(numeros % 23)
        return dni[8] == diccionarioLetras[resto]