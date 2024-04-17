from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException

class ReservationJsonStore(JsonStore):
    _file_name = JSON_FILES_PATH + "store_reservation.json"

