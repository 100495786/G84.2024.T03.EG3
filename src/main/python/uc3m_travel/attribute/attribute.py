from uc3m_travel.hotel_management_exception import HotelManagementException
import re

class Attribute:

    _regex_pattern = ""
    _error_message = ""
    _attr_value = ""

    def _validate(self, attr_value):
        r = self._regex_pattern
        myregex = re.compile(r)
        resultado = myregex.fullmatch(attr_value)
        if not resultado:
            raise HotelManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value
