from uc3m_travel.attribute.attribute import Attribute
from uc3m_travel.hotel_management_exception import HotelManagementException


class NumDays(Attribute):
    def __init__(self, attr_value):
        self._regex_pattern = ""
        self._error_message = ""
        self._attr_value = self._validate(attr_value)

    def _validate(self, num_days):
        """validates the number of days"""
        try:
            days = int(num_days)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise HotelManagementException("Numdays should be in the range 1-10")
        return num_days
