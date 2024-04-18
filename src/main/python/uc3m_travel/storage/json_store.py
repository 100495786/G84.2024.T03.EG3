from uc3m_travel.hotel_management_exception import HotelManagementException
import json
class JsonStore:
    def __init__(self):
        self._file_name=""
        self._data_list=""
        self._error_message_find = ""
        self._error_message_not_found= ""

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
        self._data_list.append(my_reservation.__dict__)

    def find_item_in_store(self, my_reservation):
        for item in self._data_list:
            if my_reservation.localizer == item["_HotelReservation__localizer"]:
                raise HotelManagementException("Reservation already exists")
            if my_reservation.id_card == item["_HotelReservation__id_card"]:
                raise HotelManagementException("This ID card has another reservation")