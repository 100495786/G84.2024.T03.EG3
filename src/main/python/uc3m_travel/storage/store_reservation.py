from uc3m_travel.storage.json_store_father import JsonStoreFather
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
class StoreReservation(JsonStoreFather):
    def __init__(self):
        self._file_name= JSON_FILES_PATH + "store_reservation.json"

