from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
class StoreCheckout(JsonStore):
    def __init__(self):
        self._file_name= JSON_FILES_PATH + "store_check_out.json"