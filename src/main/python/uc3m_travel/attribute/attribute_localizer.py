from uc3m_travel.attribute.attribute import Attribute

class Localizer(Attribute):
    def __init__(self, attr_value):
        self._regex_pattern = r'^[a-fA-F0-9]{32}$'
        self._error_message = "Invalid localizer"
        self._attr_value = self._validate(attr_value)
