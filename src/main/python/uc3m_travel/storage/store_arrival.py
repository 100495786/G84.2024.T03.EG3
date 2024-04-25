from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
import json
class StoreArrival(JsonStore):
    class __StoreArrival(JsonStore):
        _file_name = JSON_FILES_PATH + "store_check_in.json"
        _data_list = []
        _error_message_find = "ckeckin  ya realizado"

        def read_input_data_from_file(self, input_list):
            try:
                my_localizer = input_list["Localizer"]
                my_id_card = input_list["IdCard"]
            except KeyError as e:
                raise HotelManagementException("Error - Invalid Key in JSON") from e
            return my_id_card, my_localizer
        def read_input_file(self, file_input):
            try:
                with open(file_input, "r", encoding="utf-8", newline="") as file:
                    input_list = json.load(file)
            except FileNotFoundError as ex:
                raise HotelManagementException("Error: file input not found") from ex
            except json.JSONDecodeError as ex:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
            return input_list
        def find_item_in_store(self, value, key):
            self.load_json_store()
            super().find_item_in_store(value,key)
            self._error_message_find

    __instance = None
    def __new__(cls):
        if not StoreArrival.__instance:
            StoreArrival.__instance = StoreArrival.__StoreArrival()
        return StoreArrival.__instance
