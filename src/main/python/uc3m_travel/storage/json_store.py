from uc3m_travel.hotel_management_exception import HotelManagementException
import json
class JsonStore():
    _data_list = []
    _file_name = ""
    def __init__(self):
        pass
    def load_json_store(self, file_store):
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data_list

    def save_store(self, data_list, file_store):
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

    def add_item_in_store(self, data_list, my_reservation):
        data_list.append(my_reservation.__dict__)

    def find_item_in_store(self, data_list, my_reservation):
        for item in data_list:
            if my_reservation.localizer == item["_HotelReservation__localizer"]:
                raise HotelManagementException("Reservation already exists")
            if my_reservation.id_card == item["_HotelReservation__id_card"]:
                raise HotelManagementException("This ID card has another reservation")