from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
from datetime import datetime
from freezegun import freeze_time
import json
class StoreCheckout(JsonStore):
    class __StoreCheckout(JsonStore):
        _file_name = JSON_FILES_PATH + "store_check_out.json"
        _data_list = []
        _error_message_find = "Guest is already out"

        def find_checkout(self, value, key):
            self.load_json_store()
            super().find_item_in_store(value,key)
            self._error_message_find

        def create_checkout(self, room_key):
            room_checkout = {"_HotelDeparture__room_key": room_key, "_HotelDeparture__checkout_time": datetime.timestamp(datetime.utcnow())}
            return room_checkout

        def add_checkout_store(self, room_checkout):
            self._data_list.append(room_checkout)

    __instance = None
    def __new__(cls):
        if not StoreCheckout.__instance:
            StoreCheckout.__instance = StoreCheckout.__StoreCheckout()
        return StoreCheckout.__instance