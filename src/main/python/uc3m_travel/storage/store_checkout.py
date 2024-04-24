from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
import json
class StoreCheckout(JsonStore):
    def __init__(self):
        self._file_name= JSON_FILES_PATH + "store_check_out.json"
        self._data_list = []
    def load_checkin_store(self, file_store):
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: store checkin not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return room_key_list