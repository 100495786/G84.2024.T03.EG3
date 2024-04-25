from uc3m_travel.hotel_management_exception import HotelManagementException
import json
class JsonStore:
    _file_name = ""
    _data_list = []
    _error_message_find = ""
    _error_message_not_found = ""
    def __init__(self):
        pass

    def load_json_store(self):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self._data_list

    def save_store(self):
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

    def add_item_in_store(self,my_reservation):
        #self.load_json_store(self._file_name)
        self._data_list.append(my_reservation.__dict__)
        #self.save_store(self._file_name)

    def find_item_in_store(self, value, key):
        # for item in self._data_list:
        #     if my_reservation.localizer == item["_HotelReservation__localizer"]:
        #         raise HotelManagementException("Reservation already exists")
        #     if my_reservation.id_card == item["_HotelReservation__id_card"]:
        #         raise HotelManagementException("This ID card has another reservation")
        self.load_json_store()
        for item in self._data_list:
            if value == item[key]:
                raise HotelManagementException(self._error_message_find)