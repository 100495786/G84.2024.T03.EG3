from uc3m_travel.attribute.attribute import Attribute

class RoomType(Attribute):
    def __init__(self, attr_value):
        self._regex_pattern = r"(SINGLE|DOUBLE|SUITE)"
        self._error_message = "Invalid roomtype value"
        self._attr_value = self._validate(attr_value)
