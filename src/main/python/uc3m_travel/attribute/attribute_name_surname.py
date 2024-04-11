from uc3m_travel.attribute.attribute import Attribute

class NameSurname(Attribute):
    def __init__(self, attr_value):
        self._regex_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid name format"
        self._attr_value = self._validate(attr_value)



