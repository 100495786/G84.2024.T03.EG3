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
        def load_checkin_store(self, file_store):
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    room_key_list = json.load(file)
            except FileNotFoundError as ex:
                raise HotelManagementException("Error: store checkin not found") from ex
            except json.JSONDecodeError as ex:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
            return room_key_list
        def find_checkin(self, room_key, room_key_list):
            for item in room_key_list:
                if room_key == item["_HotelStay__room_key"]:
                    return item["_HotelStay__departure"]
            raise HotelManagementException("Error: room key not found")

        def is_today_departure(self, departure_date_timestamp):
            today = datetime.utcnow().date()
            if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                raise HotelManagementException("Error: today is not the departure day")

        def find_checkout(self, room_key, room_key_list):
            for checkout in room_key_list:
                if checkout["room_key"] == room_key:
                    raise HotelManagementException("Guest is already out")

        def create_checkout(self, room_key):
            room_checkout = {"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}
            return room_checkout

        def add_checkout_store(self, room_checkout):
            self._data_list.append(room_checkout)

    __instance = None
    def __new__(cls):
        if not StoreCheckout.__instance:
            StoreCheckout.__instance = StoreCheckout.__StoreCheckout()
        return StoreCheckout.__instance