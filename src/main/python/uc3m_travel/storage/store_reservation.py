from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
class StoreReservation(JsonStore):
    def __init__(self):
        self._file_name= JSON_FILES_PATH + "store_reservation.json"
        self._data_list =[]
        self._error_message_find = "Reservation already exists"
    def find_item_in_store(self, value1, key1, value2,key2):
        self.load_json_store()
        super().find_item_in_store(value1,key1)
        self._error_message_find = "This ID card has another reservation"
        super().find_item_in_store(value2, key2)